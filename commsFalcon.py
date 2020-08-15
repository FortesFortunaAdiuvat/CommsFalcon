import requests
import argparse

from TwitterFollowBot.TwitterFollowBot import TwitterBot

my_bot = TwitterBot('config_weshawes9000.txt')

def getHandle(tweeter_id):
    headers = {
        'origin':'https://tweeterid.com'
    }
    res = requests.post('https://tweeterid.com/ajax.php', data={'input':f'{tweeter_id}'}, headers=headers)
    print(res.content.decode('utf-8'))
    return res.content.decode('utf-8')

def follow_followers():
    my_bot.auto_follow_followers()
    return
    

def sync_info():
    previous_followers = []
    with open('followers.txt', 'r') as f:
        for line in f:
            previous_followers.append(line.replace('\n',''))

    # for follower in previous_followers:
    #     print(follower)
    my_bot.sync_follows()
    current_followers = []
    with open('followers.txt','r') as f:
        for line in f:
            current_followers.append(line.replace('\n',''))
    
    # print(len(previous_followers))
    # print(len(current_followers))
    new_followers = list(set(current_followers) - set(previous_followers))
    lost_followers = list(set(previous_followers) - set(current_followers))
    with open('new_followers.txt', 'w') as f:
        for follower in new_followers:
            f.write(follower+'\n')

    with open('lost_followers.txt', 'w') as f:
        for follower in lost_followers:
            f.write(follower+'\n')

    # print(f'{len(new_followers)} New Followers:\n{new_followers}')
    # print(f'{len(lost_followers)} Lost Followers:\n{lost_followers}')
    # new_followers = [x for x in set(previous_followers) if x not in set(current_followers)]
    # print(new_followers)
    return

def follow_users_followers(user_to_follow):
    my_bot.auto_follow_followers_of_user(user_to_follow, count=10)
    return


def unfollow_nonfollowers():
    my_bot.auto_unfollow_nonfollowers()
    return

def followPrompts():
    syncOption = input('Sync Account Info (y/n)? ')
    if syncOption == 'y':
        print('Syncing Account Info To Local Cache for Twitter Handle ')
        my_bot.sync_follows()
    else:
        print('Skipping Account Info Sync.')

    follow_followers_option = input('Follow back your followers (y/n)? ')
    if follow_followers_option == 'y':
        print('Following back current Followers...')
        my_bot.auto_follow_followers()
    else:
        print('Skipping Follow Back Followers.')

    follow_followers_of_user_option = input('Follow users of a specific user (y/n)? ')
    if follow_followers_of_user_option == 'y':
        user_to_follow = input('Enter User Twitter Handle, without the "@": ')
        my_bot.auto_follow_followers_of_user(user_to_follow, count=1000)
    else:
        print('Skipping Follow Followers of User.')

    unfollow_nonfollowers_option = input('Unfollow Non-Followers (y/n)? ')
    if unfollow_nonfollowers_option == 'y':
        print('Unfollowing Non-Followers...')
        my_bot.auto_unfollow_nonfollowers()
    else:
        print('Skipping Unfollowing Non-Followers')


    print('Done.')

    return

#create argument parser
my_parser = argparse.ArgumentParser(description='Display options for CommsFalcon Twitter CLI')

# CLI arguments
user_list = []; tweeter_id_list = [] 
my_parser.add_argument('-s','--syncInfo', action='store_true',help='Needed to save on API rate limits and faster analysis. Creates local cache of your followers, your following.')
my_parser.add_argument('-f','--followFollowers', action='store_true', help='Follow Back Your Followers.')
my_parser.add_argument('-u','--followUsersFollowers', action='store',type=str,metavar=user_list, nargs='+',help='Follow The Followers of a specified user. Do not include @ symbol. Multiple users can be given spearated by a space.')
my_parser.add_argument('-r','--unfollowNonFollowers', action='store_true', help='Remove/Unfollow Users You Follow Who Do Not Follow You Back.')
my_parser.add_argument('-c','--convertTweeterID', action='store', type=int, metavar=tweeter_id_list, nargs='+', help='Given unique TweeterID, returns users Handle')
my_parser.add_argument('-m','--messageDirect', action='store_true', help='Send direct message to user')

# parse CLI arguments at run time
args = my_parser.parse_args()

if args.syncInfo:
    print('syncinfo...')
    sync_info()
    print('Done.')

if args.followFollowers:
    print('Following Back Your Followers...')
    follow_followers()
    print('Done.')

if args.followUsersFollowers:
    print('Following User(s) Followers....')
    for user in user_list:
        follow_users_followers(user)
    print('Done.')

if args.unfollowNonFollowers:
    print('Unfollowing Users Who Dont Follow You...')
    unfollow_nonfollowers()
    print('Done.')

if args.convertTweeterID:
    print('Converting TweeterID(s)...')
    for tweeter_id in tweeter_id_list:
        getHandle(tweeter_id)
    print('Done.')

