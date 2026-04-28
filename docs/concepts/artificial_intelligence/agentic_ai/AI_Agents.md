## Intro to AI Agents

### Description

- An AI agent essentially is derived from two different sets of context.

1. It's a term that is commonly used in the field of reinforcement learning.

- Some subject that is part of an environment. There is a task that the subject has to perform. If the subject performs the task well, there is a reward given to the subject. If the reward is constantly occurring, the patterns or policies that define how the subject is performing task is what we consider as "learning".

2. The second context is that an agent refers to a large language model that has the ability to take instructions and break it down into step-by-step procedures with the ability to interact with tools similar to how a human interacts with tools.

- Reasoning and Acting (ReAct)

> Determine NVIDIA's closing stock price 5 days from now.

#### Chain of Thought

1. What is the current date?

2. Does the closing price already exist 5 days from the current date?

- Web Search

3. I cannot find the closing price 5 days by just searching so then you revert into what the user might be thinking which might be more of "predicting" the price rather than knowing it.

4. Do I have access to any tools that allow me to predict the price 5 days later?

5. No tools currently available to do this so I am just going to tell the user that I cannot determine NVIDIA's closing stock price 5 days of now.

