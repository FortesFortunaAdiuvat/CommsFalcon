import requests

from TwitterFollowBot.TwitterFollowBot import TwitterBot

my_bot = TwitterBot('')

syncOption = input('Sync Account Info? y/n')
if syncOption == 'y':
    print('Syncing Account Info To Local Cache for Twitter Handle ')
    my_bot.sync_follows()
else:
    print('Skipping Account Info Sync.')

follow_followers_option = input('Follow back your followers? y/n')
if follow_followers_option == 'y':
    print('Following back current Followers...')
    my_bot.auto_follow_followers()
else:
    print('Skipping Follow Back Followers.')

follow_followers_of_user_option = input('Follow users of a specific user? y/n')
if follow_followers_of_user_option == 'y':
    user_to_follow = input('Enter User Twitter Handle, without the "@": ')
    my_bot.auto_follow_followers_of_user(user_to_follow, count=1000)
else:
    print('Skipping Follow Followers of User.')

unfollow_nonfollowers_option = input('Unfollow Non-Followers? y/n')
if unfollow_nonfollowers_option == 'y':
    print('Unfollowing Non-Followers...')
    my_bot.auto_unfollow_nonfollowers()
else:
    print('Skipping Unfollowing Non-Followers')


print('here')


