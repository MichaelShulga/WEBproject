import argparse

params = argparse.ArgumentParser()
params.add_argument('--heroku', action='store_true')
args = params.parse_args()

print(args.heroku)
