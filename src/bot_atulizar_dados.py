import csv
from pybot import *

with open('flights.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    time.sleep(1.5)
    for row in spamreader:
        print(', '.join(row))

        bot = Bot(
            triggersAndActions=[
                TriggerAndAction(
                    trigger=TriggerPrintPoint(
                        position=PixelPosition(x=0, y=0),
                        color=Color(r=0, g=0, b=0),
                    ),
                    action=ActionCompound(
                        actionSequence=[
                            ActionMouseMove(aim=PixelPosition(x=10, y=10),),
                            ActionClick(),
                            ActionWaitDuration(durationMilliseconds=150),
                            ActionMouseMove(aim=PixelPosition(x=30, y=250),),
                            ActionClick(),
                            ActionMouseMove(aim=PixelPosition(x=1380, y=240),),
                            ActionClick(),
                        ]
                    ),
                ),
            ],
            stepIntervalMilliseconds=300,
            builderPerception=BuilderPerception()
        )

        bot.run()
