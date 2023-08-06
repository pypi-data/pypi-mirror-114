
"""
    Title: reset.py
    Module Name: reset.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ## Reset/ rollback function     ## 
         ###############################################################
 """
import git
import os
import click
import git
import sys
from github import Github


@click.command()
@click.option('--token', '-e', default="dev", prompt='Enter token ', help='Roll back to the previous version')
def reset(token):
  """Roll back to the previous version"""
    
  """
    param : token is the argument which is a aceess token for getting access to the
    github repository.
    Variables Used:
    token : Stores the github access token 
    repo : stores the reposirory 
    
    return: Nil
  """
  g=Github(token)
  name=input("Enter the repo name")
  repo_name="AkashAi7/"+name
  repo = git.Repo(repo_name)
  repo.git.reset('--hard')