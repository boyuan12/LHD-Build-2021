from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot(
    "CovAid",
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ]
)

# create a ListTrainer
trainer = ListTrainer(chatbot)

trainer.train(["What's Local Hack Day?", "Local Hack Day is the best hacking event in the world!"])
trainer.train(["How can I join?", "Go to https://lhd.mlh.io"])