
"""
    Title: allrepo.py
    Module Name: allrepo.py
    Author: Akash Dwivedi
    Language: Python
    Date Created: 26-07-2021
    Date Modified: 29-07-2021
    Description:
        ###############################################################
        ## Display Avaialable Reposirot   ## 
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
def allrepo(token):
    '''Shows all the repo in the account '''
    """
    param : token is the argument which is a aceess token for getting access to the
    github repository.
    Variables Used:
    token : Stores the github access token 
    repo : stores the reposirory 
    
    return: Nil
    """
    print('Choose the repo type ')
    g=Github(token)
    print(g)
    i=1
    for repo in g.get_user().get_repos():
     print(i," ",repo.name)
     i=i+1