"""
pScheduler Limit Processor
"""

import os
import pscheduler

from identifierset  import IdentifierSet
from classifierset  import ClassifierSet
from limitset       import LimitSet
from applicationset import ApplicationSet

class LimitProcessor():

    """
    pScheduler limit processing class
    """


    def __init__(self,
                 source=None  # Open file or path to file with limit set
    ):
        """Construct a limit processor.

        The 'source' argument can be one of three types:

        string - Path to a file to open and read.

        file - Open file handle to read.

        None - The limit processor becomes inert and passes all limits
        unconditionally.
        """

        # If we were given no source, put the processor into an inert
        # mode where everything passes.
        self.inert = source is None
        if self.inert:
            return


        #
        # Load the validation data
        #

        validation_path = os.path.join(os.path.dirname(__file__),
                                       'pscheduler-limits-validate.json')
        # TODO: Throw something nicer than IOError if this fails.
        validation_file = open(validation_path, 'r')
        validation = pscheduler.json_load(validation_file)
        validation_file.close()

        #
        # Inhale the source and validate it
        #

        if type(source) is str or type(source) is unicode:
            source = open(source, 'r')
        elif type(source) is file:
            pass  # We're good with this.
        else:
            raise ValueError("Source must be a file or path")

        # At this point, source is a file.

        assert type(source) is file
        limit_config = pscheduler.json_load(source)

        valid, message = pscheduler.json_validate(limit_config, validation)

        if not valid:
            raise ValueError("Invalid limit file: %s" % message)

        #
        # Set up all of the stages
        #

        self.identifiers  = IdentifierSet(limit_config['identifiers'])
        self.classifiers  = ClassifierSet(limit_config['classifiers'],
                                          self.identifiers)
        self.limits       = LimitSet(limit_config['limits'])
        self.applications = ApplicationSet(limit_config['applications'],
                                           self.classifiers, self.limits)



    def process(self, task, hints):
        """Evaluate a proposed task against the full limit set.

        If the task has no 'schedule' section it will be assumed that
        is being evaluated on all other parameters except when it
        runs.  (This will be used for restricting submission of new
        tasks.)

        Arguments:
            task - The proposed task
            hints - A hash of the hints to be used in identification

        Returns a tuple containing:
            passed - True if the proposed task passed the limits applied
            diags - A textual summary of how the conclusion was reached
        """

        if self.inert:
            return True, "No limits were applied"


        # TODO: Consider checking to see if the source file has
        # changed and reloading it if it has.

        # TODO: Should this be JSON, or is text sufficient?
        diags = []

        identifications = self.identifiers.identities(hints)
        if not identifications:
            diags.append("Made no identifications.")
            return False, '\n'.join(diags)
        diags.append("Identified as %s" % (', '.join(identifications)))

        classifications = self.classifiers.classifications(identifications)
        if not classifications:
            diags.append("Made no classifications.")
            return False, '\n'.join(diags)
        diags.append("Classified as %s" % (', '.join(classifications)))

        check_schedule='schedule' in task

        passed, app_diags = self.applications.check(task,
                                                    classifications,
                                                    check_schedule)

        diags.append(app_diags)

        diags.append("Proposal %s limits" % ("meets" if passed else "does not meet"))

        return passed, '\n'.join(diags)





# Test program

if __name__ == "__main__":

    # TODO: This should refer to a sample file in the distribution
    processor = LimitProcessor('pscheduler-limits.json')

    passed, diags = processor.process(
        {
            "type": "rtt",
            "spec": {
                "schema": 1,
                "count": 50,
                "dest": "www.perfsonar.edu"
            },
            "schedule": {
                "start": "2016-06-15T14:33:38-04",
                "duration": "PT20S"
            }
        },
        {
            "#ip": "10.0.0.7",        "#": "Dev VM",
            "#ip": "128.82.4.1",      "#": "Nobody in particular",
            "#ip": "198.51.100.3",    "#": "Hacker",
            "#ip": "62.40.106.13",    "#": "GEANT",
            "#ip": "140.182.44.164",  "#": "IU",
            "ip": "192.52.179.242",   "#": "Internet2",
        })

    print passed
    print diags

