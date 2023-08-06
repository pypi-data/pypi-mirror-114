import logging
import re
import pandas as pd
import csv

log = logging.getLogger(__name__)


def save_all_intended_fors(bc, intendedfors_writer, new=None):
    """Write all info about IntendedFors to csv file.

    Args:
        bc (BIDSCuration)
        intendedfors_writer (csv writer)
        new (bc.all_intended_fors) use this one if it is provided
    """

    for subj_label in bc.all_intended_for_dirs:

        for fmap_fname, folder_names in bc.all_intended_for_dirs[subj_label].items():

            log.debug(
                f"{bc.all_intended_for_acq_label[subj_label][fmap_fname]}, {fmap_fname}"
            )
            intendedfors_writer.writerow(
                [bc.all_intended_for_acq_label[subj_label][fmap_fname],
                 fmap_fname,
                 bc.all_df.loc[(bc.all_df['Subject'] == subj_label) &
                               (bc.all_df['File name'] == fmap_fname),
                               'Curated BIDS path'].item()]
            )

            for folder_name in folder_names:
                log.debug(f",{folder_name['Folder']}")
                intendedfors_writer.writerow([" ", folder_name["Folder"]])
                bc.all_intended_fors[subj_label][fmap_fname].sort()

                if new is None:
                    ifs_to_use = bc.all_intended_fors
                else:
                    ifs_to_use = new

                for intended_for in ifs_to_use[subj_label][fmap_fname]:
                    what_to_find = f"/{folder_name['Folder']}/"
                    if what_to_find in intended_for:
                        log.debug(f",,{intended_for}")
                        intendedfors_writer.writerow([" ", " ", intended_for])


def filter_intended_fors(fw, bc, intended_for_regexes):
    """Use pairs of regexes to match field maps with the files they modify.

    The first regular expression in each pair matches the field map name, and the
    second regex matches the IntendedFor (relative path to file).  IntendedFors are
    kept only when both regexes match.

    Args:
        fw (Flywheel Client)
        bc (BIDSCuration)
        intended_for_regexes (list): pairs of regular expressions

    Returns:
        new_intended_fors (list of strings): for each field map, list of paths to files it modifies
    """

    ifr = intended_for_regexes.split(" ")
    string_pairs = zip(ifr[::2], ifr[1::2])
    # for pair in string_pairs:
    #    print(f"fmap regex \"{pair[0]}\" will correct file \"{pair[1]}\"")

    regex_pairs = list()
    for s_p in string_pairs:
        regex_pairs.append([re.compile(s_p[0]), re.compile(s_p[1])])

    new_intended_fors = dict()

    for subj_label in bc.all_intended_fors:

        new_intended_fors[subj_label] = dict()

        for fmap_fname, acquisition_label in bc.all_intended_for_acq_label[
            subj_label
        ].items():
            log.debug(f"{acquisition_label}")

            for regex in regex_pairs:

                if regex[0].search(acquisition_label):

                    new_intended_fors[subj_label][fmap_fname] = list()

                    for i_f in bc.all_intended_fors[subj_label][fmap_fname]:
                        if regex[1].search(i_f):
                            log.debug(f"found {i_f}")
                            new_intended_fors[subj_label][fmap_fname].append(i_f)

                    fw.modify_acquisition_file_info(
                        bc.all_intended_for_acq_id[subj_label][fmap_fname],
                        fmap_fname,
                        {
                            "set": {
                                "IntendedFor": new_intended_fors[subj_label][fmap_fname]
                            }
                        },
                    )

    return new_intended_fors


def get_most_subjects_count(acquisition_labels, subjects_have):
    # for each acquisition label find the number of times it appears for most subjects
    # subjects_have[subject.label][acquisition.label] = count
    # most_subjects_have_count[acquisition.label][count] will be a count histogram
    # there has to be a better way of doing this
    most_subjects_have_count = dict()

    # go through all subjects
    for subj_label in subjects_have:

        # and all acquisition labels found in any subject
        for acq_label in acquisition_labels:

            # create the "histogram"
            if acq_label not in most_subjects_have_count:
                most_subjects_have_count[acq_label] = dict()

            if acq_label in subjects_have[subj_label]:

                count = subjects_have[subj_label][acq_label]

                if count in most_subjects_have_count[acq_label]:
                    most_subjects_have_count[acq_label][count] += 1
                else:
                    most_subjects_have_count[acq_label][count] = 1

            else:  # label not seen for subject so count # of times it was missing
                if 0 in most_subjects_have_count[acq_label]:
                    most_subjects_have_count[acq_label][0] += 1
                else:
                    most_subjects_have_count[acq_label][0] = 1

    return most_subjects_have_count


COLUMNS = (
    "Subject",
    "Session",
    "SeriesNumber",
    "Ignored",
    "Rule ID",
    "Acquisition label (SeriesDescription)",
    "File name",
    "File type",
    "Curated BIDS path",
    "Unique?",
)


class BIDSCuration:
    """Representation of Flywheel metadata BIDS Curation."""

    def __init__(self):
        self.all_df = pd.DataFrame(columns=COLUMNS)

        # Counts of particular acquisitions
        # acquisition_labels[acquisition.label] = count over entire project
        self.acquisition_labels = dict()

        # subjects_have[subject.label][acquisition.label] = count for this subject
        self.subjects_have = dict()

        # See get_bids.py for a description of what these hold
        self.all_intended_for_acq_label = dict()
        self.all_intended_for_acq_id = dict()
        self.all_intended_for_dirs = dict()
        self.all_intended_fors = dict()

        self.all_seen_paths = dict()

        self.most_subjects_have = dict()

    def save_niftis(self, pre_path):
        """Save acquisition/file name -> bids path mapping. """

        self.all_df.to_csv(f"{pre_path}_niftis.csv", index=False)

    def save_intendedfors(self, pre_path, verbose, intended_for_regexes, fw):
        """save field map IntendedFor lists.

        If intended_for_regexes has been provided (a list of regex pairs), this method will only keep the ones that match
        """

        with open(f"{pre_path}_intendedfors.csv", mode="w") as intendedfors_file:
            intendedfors_writer = csv.writer(
                intendedfors_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            intendedfors_writer.writerow(
                [
                    "acquisition label",
                    "file name and folder",
                    "IntendedFors: List of relative BIDS paths",
                ]
            )

            save_all_intended_fors(self, intendedfors_writer)

            # Keep only proper file paths if they match field maps as per provided regexes
            if intended_for_regexes:

                new_intended_fors = filter_intended_fors(fw, self, intended_for_regexes)

                if verbose > 0:
                    intendedfors_writer.writerow(
                        ["Final values (after correction using regexes)"]
                    )

                # write out final values of IntendedFor lists
                intendedfors_writer.writerow(
                    [
                        " ",
                        " ",
                        " ",
                    ]
                )
                intendedfors_writer.writerow(
                    [
                        "acquisition label",
                        "file name and folder",
                        "IntendedFor List of BIDS paths",
                    ]
                )

                # Write out intended_fors again since they were filtered
                save_all_intended_fors(self, intendedfors_writer, new=new_intended_fors)

    def save_acquisition_details(self, num_subjects, num_sessions, pre_path):
        """Save acquisition labels count list."""

        with open(
            f"{pre_path}_acquisitions_details_1.csv", mode="w"
        ) as acquisition_file:
            acquisition_writer = csv.writer(
                acquisition_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            acquisition_writer.writerow(["Number of subjects", num_subjects])
            acquisition_writer.writerow(["Number of sessions", num_sessions])
            acquisition_writer.writerow([])

            acquisition_writer.writerow(
                ["Unique acquisition label", "total number found"]
            )
            for label, count in self.acquisition_labels.items():
                acquisition_writer.writerow([label, count])

            most_subjects_have_count = get_most_subjects_count(
                self.acquisition_labels, self.subjects_have
            )

            acquisition_writer.writerow([])
            acquisition_writer.writerow(["Acquisition label", "Usual count"])

            # the max of the counts for an acquisition label is what most subjects have
            for acq_label in self.acquisition_labels:
                max_count = 0
                max_index = 0
                for count, num_count in most_subjects_have_count[acq_label].items():
                    if num_count > max_count:
                        max_count = num_count
                        max_index = count
                self.most_subjects_have[acq_label] = max_index

                acquisition_writer.writerow([acq_label, max_index])

        with open(
            f"{pre_path}_acquisitions_details_2.csv", mode="w"
        ) as acquisition_file:
            acquisition_writer = csv.writer(
                acquisition_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            acquisition_writer.writerow(
                ["Subject", "Acquisition", "Count != to", "Usual count"]
            )

            for subj_label in self.subjects_have:
                found_problem = False
                acquisition_writer.writerow([subj_label])
                for acq_label in self.acquisition_labels:
                    if acq_label in self.subjects_have[subj_label]:
                        if (
                            self.subjects_have[subj_label][acq_label]
                            != self.most_subjects_have[acq_label]
                        ):
                            found_problem = True
                            acquisition_writer.writerow(
                                [
                                    " ",
                                    acq_label,
                                    self.subjects_have[subj_label][acq_label],
                                    self.most_subjects_have[acq_label],
                                ]
                            )
                    else:
                        if self.most_subjects_have[acq_label] != 0:
                            found_problem = True
                            acquisition_writer.writerow(
                                [
                                    " ",
                                    acq_label,
                                    0,
                                    self.most_subjects_have[acq_label],
                                ]
                            )
                if not found_problem:
                    acquisition_writer.writerow(
                        [
                            " ",
                            "Subject has all of the usual acquisitions, no  more, no less!",
                        ]
                    )

        return most_subjects_have_count

    def save_acquisitions(self, pre_path):
        """Save typical acquisitions and lists of good/bad subjects."""

        with open(f"{pre_path}_acquisitions.csv", mode="w") as acquisition_file:
            acquisition_writer = csv.writer(
                acquisition_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            acquisition_writer.writerow(["Acquisition Label", "Usual Count"])
            for acq_label, usual_count in self.most_subjects_have.items():
                if usual_count > 0:
                    acquisition_writer.writerow([acq_label, usual_count])

            acquisition_writer.writerow([])
            acquisition_writer.writerow(
                ["Subjects that have all of the Typical Acquisitions"]
            )
            troubled_subjects = dict()
            has_no_errors = list()
            for subj_label in self.subjects_have:
                no_errors = True
                warnings = False
                troubled_subjects[subj_label] = list()
                for acq_label, usual_count in self.most_subjects_have.items():
                    if acq_label not in self.subjects_have[subj_label]:
                        if usual_count > 0:
                            no_errors = False
                            troubled_subjects[subj_label].append(
                                f"ERROR: missing {acq_label}"
                            )
                    else:
                        subj_has = self.subjects_have[subj_label][acq_label]
                        most_have = self.most_subjects_have[acq_label]
                        if subj_has < most_have:
                            no_errors = False
                            troubled_subjects[subj_label].append(
                                f"ERROR: not enough {acq_label} acquisitions.  Found {subj_has}, most have {most_have}"
                            )
                        elif subj_has > most_have:
                            warnings = True
                            if usual_count > 0:
                                troubled_subjects[subj_label].append(
                                    f"WARNING: too many {acq_label} acquisitions?  Found {subj_has}, most have {most_have}"
                                )
                            else:
                                troubled_subjects[subj_label].append(
                                    f"WARNING: extra {acq_label} acquisition(s)?  Found {subj_has}, most subjects don't have this."
                                )
                if no_errors:
                    has_no_errors.append(subj_label)
                    acquisition_writer.writerow([subj_label])
                    if warnings:
                        for warning in troubled_subjects[subj_label]:
                            acquisition_writer.writerow([" ", warning])
                    else:
                        acquisition_writer.writerow(
                            [
                                " ",
                                "This subject has all of the typical acquisitions, no more, no less.",
                            ]
                        )

            acquisition_writer.writerow([])
            acquisition_writer.writerow(
                ["Subjects that don't have Typical Acquisitions"]
            )
            for subj_label, bad_news in troubled_subjects.items():
                if subj_label in has_no_errors:
                    pass
                else:
                    acquisition_writer.writerow([subj_label])
                    for news in bad_news:
                        acquisition_writer.writerow([" ", news])
