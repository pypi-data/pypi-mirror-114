# KeySpot
Sign up [here](https://keyspot.app)

KeySpot is a tool to help manage environment variables for individuals and teams of developers. The service stores environment variables for your project in a centralized place so you don't have to juggle different .env files for your environements and applications. Once you have signed in at [keyspot.app](https://keyspot.app), you can create new records, share them with your team, and access them in code.

See our [usage tutorial]() on YouTube.

# Installation

```bash
$ pip install keyspot
```

# Usage

Sign in to [KeySpot](https://keyspot.app), and create a record. At the top of each record's page there is an accessKey. Copy the accessKey as you will be using this to access your environment variables in code.

Accessing your environment in code:
```python
import keyspot

record = keyspot.get_record('<accessKey>')
```

Updating your environment in code:
```python
import keyspot

newVariables = {"newVar1": "foo", "newVar2": "bar"}

update_record('<accessKey>', newVariables)

```

note: You will want to supply your program with your access key as your only environement variable or a command line argument.

