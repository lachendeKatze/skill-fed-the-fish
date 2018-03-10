# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

import time
import pytz
import datetime

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.configuration.config import Configuration
from mycroft.util.log import LOG, getLogger

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

LOGGER = getLogger(__name__)

# TODO: Change "Template" to a unique name for your skill
class FedTheFishSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(FedTheFishSkill, self).__init__(name="FedTheFishSkill")
        
        # Initialize working variables used within the skill.
        self.count = 0
	self.myTimeZone = (Configuration.get())["location"]["timezone"]["code"]

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    @intent_handler(IntentBuilder("").require("Fed").require("Fish"))
    def handle_fed_fish_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak_dialog("fed.fish")

	utc_now   = pytz.utc.localize(datetime.datetime.utcnow())
	time_now  = utc_now.astimezone(pytz.timezone(self.myTimeZone))
	timeString = time_now.strftime("%A %B %d %I %M %p") + "\n"	

	with open(self.settings["log_location"] + "mostRecent.log", "w") as logFile:
		logFile.write(timeString)
		logFile.close()
	
	with open(self.settings["log_location"] + "fedHistory.log", "a") as logFile:
		logFile.write(timeString)
		logFile.close()


    @intent_handler(IntentBuilder("").require("Has").require("Fish").require("Fed"))
    def handle_was_fed(self, message):
	
	utc_now   = pytz.utc.localize(datetime.datetime.utcnow())
	time_now  = utc_now.astimezone(pytz.timezone(self.myTimeZone))

       	with open(self.settings["log_location"] + "mostRecent.log", "r") as logFile:
		lastFed = (logFile.readline()).split(' ')
		logFile.close
		
	dayFed = lastFed[2].lstrip('0') # remove a leading 0
	monthFed = lastFed[1]
	# LOGGER.info(" ***** " + lastFed )
	LOGGER.info(" ***** " + dayFed )
	LOGGER.info(" ***** " + monthFed )	
	
	if (int(dayFed) == int(time_now.strftime("%d"))) and (monthFed == time_now.strftime("%B")):
		self.speak("yes the fish was fed today")
	else:
		self.speak("no the fish was not fed today")
		

        # self.speak_dialog("count.is.now", data={"count": self.count})

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #     return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return FedTheFishSkill()

