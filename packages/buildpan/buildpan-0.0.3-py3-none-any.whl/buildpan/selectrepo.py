
"""
    Title: selectrepo.py
    Module Name: allrepo.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ## Selects a specific repository   ## 
         ###############################################################
 """
import git
import os
import click
import git
import sys
from github import Github


@click.command()
@click.option('--token', '-e', default="dev", prompt='Enter token ', help='Shows all the repo in the account')

def selectrepo(token):
    '''Select the repo in the account '''
    """
    param : token is the argument which is a aceess token for getting access to the
    github repository.
    Variables Used:
    token : Stores the github access token 
    repo : stores the reposirory 
    content: Stores the files avaialable in the files in the repository
    return: Nil
    """
    g=Github(token)
    print(g)
    i=1
    for repo in g.get_user().get_repos():
     print(i," ",repo.name)
    i=i+1
    name=input("Enter the repo name")
    repo=g.get_repo("AkashAi7/"+name)
    reponame="AkashAi7/"+name
    print(reponame)
    content=repo.get_contents("")
    for file in content:
       print("FILE NAME ARE ",file)
   