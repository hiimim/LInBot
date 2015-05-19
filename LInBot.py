#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, random, sys, time, urlparse
from selenium import webdriver
from bs4 import BeautifulSoup

def Launch():
    # Check if the file 'config' exists, otherwise quit
    if os.path.isfile('config') == False:
        print 'Error! No configuration file.'
        sys.exit()
    
    # Check if the file 'visitedUsers.txt' exists, otherwise create it
    if os.path.isfile('visitedUsers.txt') == False:
        visitedUsersFile = open('visitedUsers.txt', 'wb')
        visitedUsersFile.close()

    # Browser choice
    print 'Choose your browser:'
    print '[1] Chrome'
    print '[2] Firefox/Iceweasel'
    print '[3] Firefox/Iceweasel (light)'
    print '[4] PhantomJS'
    print '[5] PhantomJS (light)'

    while True:
        try:
            browserChoice = int(raw_input('Choice? '))
        except ValueError:
            print 'Invalid choice.',
        else:
            if browserChoice not in [1,2,3,4,5]:
                print 'Invalid choice.',
            else:
                break

    StartBrowser(browserChoice)


def StartBrowser(browserChoice):
    if browserChoice == 1:
        print '\nLaunching Chrome'
        browser = webdriver.Chrome()

    if browserChoice == 2:
        print '\nLaunching Firefox/Iceweasel'
        browser = webdriver.Firefox()

    if browserChoice == 3:
        print '\nLaunching Firefox/Iceweasel (light)'
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        firefoxLightProfile = FirefoxProfile()
        firefoxLightProfile.set_preference('permissions.default.stylesheet', 2) # Disable CSS
        firefoxLightProfile.set_preference('permissions.default.image', 2) # Disable images
        firefoxLightProfile.set_preference('javascript.enabled', False) # Disable javascript
        firefoxLightProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False) # Disable Flash
        firefoxLightProfile.set_preference('browser.chrome.toolbar_style', 0) # Display toolbar buttons with icons only, no text
        browser = webdriver.Firefox(firefoxLightProfile)

    # -> TODO: disable log file for phantomJS!

    if browserChoice == 4:
        print '\nLaunching PhantomJS'
        browser = webdriver.PhantomJS()

    if browserChoice == 5:
        print '\nLaunching PhantomJS (light)'
        browser = webdriver.PhantomJS()
        browser.desired_capabilities['userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
        browser.desired_capabilities['javascriptEnabled'] = False
        browser.desired_capabilities['loadImages'] = False
        browser.desired_capabilities['webSecurityEnabled'] = False

    # Open, load and close the 'config' file
    with open('config', 'r') as configFile:
        config = [line.strip() for line in configFile]
    configFile.close()

    # Sign in
    browser.get('https://linkedin.com/uas/login')
    emailElement = browser.find_element_by_id('session_key-login')
    emailElement.send_keys(config[0])
    passElement = browser.find_element_by_id('session_password-login')
    passElement.send_keys(config[1])
    passElement.submit()

    print 'Signing in...'
    time.sleep(3)

    soup = BeautifulSoup(browser.page_source)
    if soup.find('div', {'class':'alert error'}):
        print 'Error! Please verify your username and password.'
        browser.quit()
    else:
        print 'Success!\n'
        LInBot(browser)


def LInBot(browser):
        T = 0
        V = 0
        profilesQueued = []

        print 'Everything starts with a random profile...\n'

        # Infinite loop
        while True:

            # Generate random IDs
            while True:
                browser.get('https://www.linkedin.com/profile/view?id='+str(random.randint(10000000, 99999999)))
                T += 1
                if GetNewProfilesID(BeautifulSoup(browser.page_source), profilesQueued):
                    break
                else:
                    print '|',
                    time.sleep(random.uniform(3, 6.5))

            soup = BeautifulSoup(browser.page_source)
            profilesQueued = GetNewProfilesID(soup, profilesQueued)
            V += 1
            print '\n\nFinally found one !\n'
            print browser.title.replace(' | LinkedIn', '')+' visited. T: '+str(T)+' | V: '+str(V)+' | Q: '+str(len(profilesQueued))

            while profilesQueued:
               
                profileID = profilesQueued.pop()
                browser.get('https://www.linkedin.com/profile/view?id='+profileID)
               
                # Add the ID to the visitedUsersFile
                with open('visitedUsers.txt', 'ab') as visitedUsersFile:
                    visitedUsersFile.write(str(profileID)+'\r\n')
                visitedUsersFile.close()

                # Get new profiles ID
                soup = BeautifulSoup(browser.page_source)
                profilesQueued.extend(GetNewProfilesID(soup, profilesQueued))

                T += 1

                try:
                    if str(browser.title).decode('utf-8') == 'Profile | LinkedIn':
                        print 'User not in your network. T: '+str(T)+' | V: '+str(V)+' | Q: '+str(len(profilesQueued))
                    else:
                        V +=1
                        print browser.title.replace(' | LinkedIn', '')+' visited. T: '+str(T)+' | V: '+str(V)+' | Q: '+str(len(profilesQueued))
                except Exception, e:
                    V +=1
                    print '(cannot decode) visited. T: '+str(T)+' | V: '+str(V)+' | Q: '+str(len(profilesQueued))
                    
                # Sleep to make sure everything loads, add random to make us look human
                time.sleep(random.uniform(3, 6.5))

            print '\nNo more profiles to visit. Everything restarts with a random profile...\n'
            

def GetNewProfilesID(soup, profilesQueued):
    # Open, load and close
    with open('visitedUsers.txt', 'r') as visitedUsersFile:
        visitedUsers = [line.strip() for line in visitedUsersFile]
    visitedUsersFile.close()

    # Get profiles from the "People Also Viewed" section
    profilesID = []
    try:
        for link in soup.find('div', {'class':'insights-browse-map'}).findAll('a', {'class':'browse-map-photo'}):
            if 'profile/view?id=' in link.get('href'):
                profileID = urlparse.parse_qs((urlparse.urlparse(link.get('href'))).query)['id'][0]
                if (profileID not in visitedUsers) and (profileID not in profilesQueued):
                    profilesID.append(profileID)
    except:
        pass
    
    return profilesID

    
if __name__ == '__main__':       
    Launch()
