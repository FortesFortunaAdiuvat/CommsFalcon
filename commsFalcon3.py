import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_auth
import dash_table
from datetime import datetime
import pandas as pd
import io, base64
import twint
import tweepy
from TwitterFollowBot.TwitterFollowBot import TwitterBot
import sqlite3, requests

USERNAME_PASSWORD_PAIRS = [
    ['JamesBond', '007']
]

class cf_bot_handler():
    def __init__(self):
        self.my_bot = TwitterBot()
        return
    def init_bot(self, config_dict):
        self.my_bot.commsFalcon_bot_setup(config_dict)
        return
    def syncData(self):
        self.my_bot.commsFalcon_sync()
        return
    def auto_fav_tweets(self, phrase):
        self.my_bot.auto_fav(phrase)
    def follow_users_followers(self, username):
        self.my_bot.commsFalcon_auto_follow_followers_of_user(username)
        return
    def follow_back_followers(self):
        self.my_bot.commsFalcon_auto_follow_followers()
        return
    def unfollow_non_followers(self):
        self.my_bot.commsFalcon_auto_unfollow_nonfollowers()
        return
    def retweet_tweets(self, phrase):
        print(phrase)
        self.my_bot.auto_rt(phrase)
        return
    def mute_follows_notifications(self):
        self.my_bot.commsFalcon_auto_mute_following()
        return
    def unmute_follows_notifications(self):
        self.my_bot.commsFalcon_auto_unmute()
        return


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets2 = ['assets/style.css']
bootstrap_themes_stylesheet = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=bootstrap_themes_stylesheet) # For CSS and custom JS: https://dash.plotly.com/external-resources
#app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)

colors = {
    'background': '#242424',
    'text': 'white',
    'monokai-red': '#f92672', #monokai classic color palette: https://www.color-hex.com/color-palette/59231
    'monokai-green': '#6e22e',
    'monokai-blue': '#66d9ef',
    'monokai-orange': '#fd971f',
    'monokai-purple': '#ae81ff'
}

# Custom button code generator: https://www.bestcssbuttongenerator.com/

sync_data_toast = html.Div([
    dbc.Toast(
        'Sync/Refresh Data Success',
        id='sync_data_toast',
        header='SUCCESS',
        is_open=False,
        dismissable=True,
        icon='success',
        duration=4000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    )
])

like_tweets_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('Auto-Fav Tweets Matching Given Phrase'),
        dbc.ModalBody(
            dbc.Form([
                dbc.Label("Phrase: "),
                dbc.Input(type='text', placeholder='#phrase_to_like', id='like_tweets_phrase_to_like'),
                dbc.Button('Execute', id='execute_like_tweets')
            ], className='like_tweets_phrase')
        ),
        dbc.ModalFooter(
            dbc.Button('Close', id='close_like_tweets')
        )
    ], id='like_tweets_modal', is_open=False, size='lg', backdrop=True, centered=True, fade=True)
])

like_tweets_toast = html.Div([
    dbc.Toast(
        "Like Tweets Job Complete.",
        id="like_tweets_toast",
        header="SUCCESS",
        is_open=False,
        dismissable=True,
        icon="success",
        #duration=4000,
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    ),
])

retweet_tweets_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('ReTweet Tweets Matching Given Phrase'),
        dbc.ModalBody(
            dbc.Form([
                dbc.Label("Phrase: "),
                dbc.Input(type='text', placeholder='#phrase_to_retweet', id='retweet_tweets_phrase_to_retweet'),
                dbc.Button('Execute', id='execute_retweet_tweets')
            ], className='retweet_tweets_phrase')
        ),
        dbc.ModalFooter(
            dbc.Button('Close', id='close_retweet_tweets')
        )
    ], id='retweet_tweets_modal', is_open=False, size='lg', backdrop=True, centered=True, fade=True)
])

retweet_tweets_toast = html.Div([
    dbc.Toast(
        "Re-Tweet Tweets Job Complete.",
        id="retweet_tweets_toast",
        header="SUCCESS",
        is_open=False,
        dismissable=True,
        icon="success",
        #duration=4000,
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    ),
])

##################################
follow_users_followers_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('Follow The Followers of a Given User...'),
        dbc.ModalBody(
            dbc.Form([
                dbc.Label("User Name: "),
                dbc.Input(type='text', placeholder='username or @twitter_handle', id='user_to_follow_followers_of'),
                dbc.Button('Execute', id='execute_follow_users_followers')
            ], className='follow_users_followers_form')
        ),
        dbc.ModalFooter(
            dbc.Button('Close', id='close_follow_users_followers')
        )
    ], id='follow_users_followers_modal', is_open=False, size='lg', backdrop=True, centered=True, fade=True)
])

follow_users_followers_toast = html.Div([
    dbc.Toast(
        "Followed Users Followers.",
        id="follow_users_followers_toast",
        header="SUCCESS",
        is_open=False,
        dismissable=True,
        icon="success",
        #duration=4000,
        # top: 66 positions the toast below the navbar
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    ),
])

follow_back_followers_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('Follow Back New Followers...'),
        dbc.ModalBody(
            dbc.Button('Confirm', id='execute_follow_back_followers')
        ),
        dbc.ModalFooter(
            dbc.Button('Close', id='close_follow_back_followers')
        )
    ], id='follow_back_followers_modal', is_open=False, size='sm', backdrop=True, centered=True, fade=True)
])

follow_back_followers_start_toast = html.Div([
    dbc.Toast(
        'Following Back New Followers....',
        id='follow_back_followers_start_toast',
        header='Running...',
        is_open=False,
        dismissable=True,
        icon='info',
        duration=4000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    ),
])

follow_back_followers_toast = html.Div([
    dbc.Toast(
        'Followed Back New Followers.',
        id='follow_back_followers_toast',
        header='SUCCESS',
        is_open=False,
        dismissable=True,
        icon='success',
        duration=4000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    ),
])
###################################
unfollow_non_followers_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('Un-Follow Users Not Following You...'),
        dbc.ModalBody(
            dbc.Button('Confirm', id='execute_unfollow_non_followers')
        ),
        dbc.ModalFooter(
            dbc.Button('Close', id='close_unfollow_non_followers')
        )
    ], id='unfollow_non_followers_modal', is_open=False, size='sm', backdrop=True, centered=True, fade=True)
])

unfollow_non_followers_toast = html.Div([
    dbc.Toast(
        'Un-Following Non-Followers...',
        id='unfollow_non_followers_toast',
        header='SUCCESS',
        is_open=False,
        dismissable=True,
        icon='info',
        duration=4000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    )
])
#################################
mute_notifications_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('Mute Notifications From Those You Follow...'),
        dbc.ModalBody(
            dbc.Button('Confirm', id='execute_mute_notifications')
        ),
        dbc.ModalFooter(
            dbc.Button('Close', id='close_mute_notifications')
        )
    ], id='mute_notifications_modal', is_open=False, size='sm', backdrop=True, centered=True, fade=True)
])

mute_notifications_toast = html.Div([
    dbc.Toast(
        'Muted Notifications.',
        id='mute_notifications_toast',
        header='SUCCESS',
        is_open=False,
        dismissable=True,
        icon='success',
        duration=4000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    )
])

unmute_notifications_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader('UnMute Notifications From Those You Follow...'),
        dbc.ModalBody(
            dbc.Button('Confirm', id='execute_unmute_notifications')
        ),
        dbc.ModalFooter(
            dbc.Button('Close', id='close_unmute_notifications')
        )
    ], id='unmute_notifications_modal', is_open=False, size='sm', backdrop=True, centered=True, fade=True)
])

unmute_notifications_toast = html.Div([
    dbc.Toast(
        'UnMuted Notifications.',
        id='unmute_notifications_toast',
        header='SUCCESS',
        is_open=False,
        dismissable=True,
        icon='success',
        duration=4000,
        style={"position": "fixed", "top": 66, "right": 10, "width": 350},
    )
])
################################
app.layout = html.Div([
    html.H1('CommsFalcon Dashboard', style={'backgroundColor':colors['background'], 'color':colors['monokai-blue'], 'textAlign':'center'}),
    html.Img(src='assets/commsFalcon_2_flipped.jpg', style={'float':'right'}),
    html.H5('STEP 1: (By uploading your API Keys, you agree I am free of any liability/consequence that may become by using this app.)', style={'color':colors['monokai-red']}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            ' ',
            html.A('Drag n\' Drop or Browse Config File')
        ]),
        style={
            'width': '36%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'color':colors['monokai-orange']
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),

    html.Div(id='output-data-upload'),
    #dbc.Input(placeholder='your handle name',type='text'), dbc.Input(placeholder='oauth token'), dbc.Input(placeholder='oauth secret'), dbc.Input(placeholder='consumer key'), dbc.Input(placeholder='consumer secret'),
    html.H5('STEP 2:', style={'color':colors['monokai-red']}),
    html.Button('Sync My Data', id='sync_button', className='myButton', n_clicks=0), #https://dash.plotly.com/dash-html-components/button
    html.P(),
    html.H5('STEP 3: PROFIT', style={'color':colors['monokai-red']}),
    html.Div([
        html.H4('~ Tweets Command Set ~', id='tweets_command_set_header', style={'color':colors['monokai-orange']}),
        dbc.Row([
            dbc.Col([
                html.Button('Like Tweets', id='like_tweets', n_clicks=0, style={'color':colors['monokai-purple']}),
                #html.Button('Search Tweets', id='search_tweets', style={'color':colors['monokai-purple']}),
                html.Button('Re-Tweet Tweets', id='retweet_tweets', style={'color':colors['monokai-purple']}),
                #html.Button('Post A Tweet', id='post_tweet', style={'color':colors['monokai-purple']})
            ]),
        ]),
        html.Div(id='like-tweets-container-output', children='')
    ]),
    
    html.Div([
        html.H4('~ Followers Command Set ~', id='followers_command_set_header', style={'color':colors['monokai-orange']}),
        dbc.Row([
            dbc.Col([
                html.Button('Follow User\'s Followers', id='follow_users_followers', style={'color':colors['monokai-purple']}),
                html.Button('Follow Back Followers', id='follow_back_followers', style={'color':colors['monokai-purple']}),
                html.Button('Un-follow Non-Followers', id='unfollow_non_followers', style={'color':colors['monokai-purple']}),
                #html.Button('Un-follow All Follows', id='unfollow_all_follows', style={'color':colors['monokai-purple']})
            ]),
        ]),
        html.Div(id='follow-users-followers-container-output', children='')
    ]),

    html.Div([
        html.H4('~ Notifications Command Set ~', style={'color':colors['monokai-orange']}),
        dbc.Row([
            dbc.Col([
                html.Button('Mute Notifications', id='mute_notifications', style={'color':colors['monokai-purple']}),
                html.Button('Un-mute Notifications',id='unmute_notifications', style={'color':colors['monokai-purple']})
            ]),
        ]),
        html.Div(id='mute_notifications_container_output', children='')
    ]),

    html.Div([
        dcc.Textarea(
            id='bot_output_textarea',
            title='Actions Executed By Bot Will Be Output Here',
            value='',
            cols=100,
            disabled=True,
            style={},
        ),

    ]),
    
    html.Div([
        #html.H4('~ Profile Metadata & Engagement Stats ~', style={'color':colors['monokai-orange']}),
    ]),

    sync_data_toast, like_tweets_modal, like_tweets_toast, 
    follow_users_followers_modal, follow_users_followers_toast,
    follow_back_followers_modal,follow_back_followers_start_toast, follow_back_followers_toast, 
    unfollow_non_followers_modal, unfollow_non_followers_toast,
    retweet_tweets_modal, retweet_tweets_toast,
    mute_notifications_modal, mute_notifications_toast,
    unmute_notifications_modal, unmute_notifications_toast,
], style={'backgroundColor':colors['background']})

# @app.callback(
#     dash.dependencies.Output('like-tweets-container-output', 'children'),
#     [dash.dependencies.Input('like_tweets', 'n_clicks')],
#     [dash.dependencies.State('input-on-submit', 'value')]
# )
# def update_output(n_clicks, value):
#     return #f'The input value was {value} and the button has been clicked {n_clicks} times. '


###### UPLOAD CALLBACK #############
def parse_contents(contents, filename, date):
    #content_type, content_string = contents.split(',')

    decoded = base64.b64decode(contents)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(
    Output('output-data-upload','children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def data_upload(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        content_type, content_string = list_of_contents.split(',')
        print(content_type)
        print(content_string)
        decoded = base64.b64decode(content_string)
        user_config_list = str(decoded.decode('utf-8')).split('\n')
        print(user_config_list)
        user_config_dict = {}
        for item in user_config_list:
            user_config_dict.update({item.split(':')[0]:item.split(':')[1]})
        
        print(user_config_dict)
        bot_handler.init_bot(user_config_dict)
 #########################################################################       
        
    #     children = []
            # parse_contents(c, n, d) for c, n, d in
            # zip(list_of_contents, list_of_names, list_of_dates)]
    return 

##### Sync Data Button Callback #####
@app.callback(
    Output('sync_data_toast', 'is_open'),
    [Input('sync_button', 'n_clicks')],
    [State('sync_data_toast', 'is_open')]
)
def sync_button(n1, is_open):
    if n1:
        bot_handler.syncData()
        return not is_open
    return is_open

################################
##### LIKE TWEETS CALLBACK #####
@app.callback(
    Output('like_tweets_modal','is_open'),
    [Input('like_tweets', 'n_clicks'), Input('close_like_tweets', 'n_clicks')],
    [State('like_tweets_modal', 'is_open')]
)
def like_tweets(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# @app.callback(
#     Output('like_tweets_toast', 'is_open'),
#     [Input('close_like_tweets', 'n_clicks')]
# )
# def open_toast(n):
#     if n:
#         return True

@app.callback(
    Output('like_tweets_toast', 'is_open'),
    [Input('execute_like_tweets', 'n_clicks')],
    [State('like_tweets_phrase_to_like', 'value')]
)
def run_like_tweets_job(n1, value):
    if value is not None:
        print(f'phrase to like is: {value}')
        bot_handler.auto_fav_tweets(value)
    if n1:
        return True 
#### ReTweet Callback ####
@app.callback(
    Output('retweet_tweets_modal','is_open'),
    [Input('retweet_tweets', 'n_clicks'), Input('close_retweet_tweets', 'n_clicks')],
    [State('retweet_tweets_modal', 'is_open')]
)
def retweet_tweets(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('retweet_tweets_toast', 'is_open'),
    [Input('execute_retweet_tweets', 'n_clicks')],
    [State('retweet_tweets_phrase_to_retweet', 'value')]
)
def run_retweet_tweets_job(n1, value):
    if value is not None:
        print(f'phrase to like is: {value}')
        bot_handler.retweet_tweets(value)
    if n1:
        return True

################################
### Follow Users Followers Callback ####
@app.callback(
    Output('follow_users_followers_modal','is_open'),
    [Input('follow_users_followers', 'n_clicks'), Input('close_follow_users_followers', 'n_clicks')],
    [State('follow_users_followers_modal', 'is_open')]
)
def follow_users_followers(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('follow_users_followers_toast', 'is_open'),
    [Input('execute_follow_users_followers', 'n_clicks')],
    [State('user_to_follow_followers_of', 'value')]
)
def follow_users_followers_job(n1, value):
    if value is not None:
        print(f'User to follow followers of: {value}')
        bot_handler.follow_users_followers(value)
    if n1:
        return True

##############################
#### Follow Back Followers Callback ####
@app.callback(
    Output('follow_back_followers_modal','is_open'),
    [Input('follow_back_followers', 'n_clicks'), Input('close_follow_back_followers', 'n_clicks')],
    [State('follow_back_followers_modal', 'is_open')]
)
def follow_back_followers(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('follow_back_followers_toast', 'is_open'),
    [Input('execute_follow_back_followers', 'n_clicks')],
    [State('follow_back_followers_toast', 'is_open')]
)
def follow_back_followers_job(n1, is_open):
    if n1 is not None:
        print(f'Following Back Followers....')
        bot_handler.follow_back_followers()
        return True
   
################################
##### Un-Follow Non-Followers Callback #####
@app.callback(
    Output('unfollow_non_followers_modal','is_open'),
    [Input('unfollow_non_followers', 'n_clicks'), Input('close_unfollow_non_followers', 'n_clicks')],
    [State('unfollow_non_followers_modal', 'is_open')]
)
def unfollow_non_followers(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('unfollow_non_followers_toast', 'is_open'),
    [Input('execute_unfollow_non_followers', 'n_clicks')],
    [State('unfollow_non_followers_toast', 'is_open')]
)
def unfollow_non_followers_job(n1, is_open):
    if n1 is not None:
        print(f'Following Back Followers....')
        bot_handler.unfollow_non_followers()
        return True
##############################
#### Mute Notifications Callback ####
@app.callback(
    Output('mute_notifications_modal','is_open'),
    [Input('mute_notifications', 'n_clicks'), Input('close_mute_notifications', 'n_clicks')],
    [State('mute_notifications_modal', 'is_open')]
)
def mute_notifications(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('mute_notifications_toast', 'is_open'),
    [Input('execute_mute_notifications', 'n_clicks')],
    [State('mute_notifications_toast', 'is_open')]
)
def mute_notifications_job(n1, is_open):
    if n1 is not None:
        print(f'Muting Notifications....')
        bot_handler.mute_follows_notifications()
        return True

##############################
#### UnMute Notifications Callback ####
@app.callback(
    Output('unmute_notifications_modal','is_open'),
    [Input('unmute_notifications', 'n_clicks'), Input('close_unmute_notifications', 'n_clicks')],
    [State('unmute_notifications_modal', 'is_open')]
)
def unmute_notifications(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('unmute_notifications_toast', 'is_open'),
    [Input('execute_unmute_notifications', 'n_clicks')],
    [State('unmute_notifications_toast', 'is_open')]
)
def unmute_notifications_job(n1, is_open):
    if n1 is not None:
        print(f'UnMuting Notifications....')
        bot_handler.unmute_follows_notifications()
        return True

#############################
#### Bot Output Textarea Callback
# @app.callback(
#     Output('bot_output_textarea', 'value'),
#     [Input()],
#     [State('bot_output_textarea','value')]
# )
# def update_bot_output_textarea(value):
#     print(value)
#     return

############################
#### SET UP ####
def ifNotExistsCreateDB():
    sqliteConnection = sqlite3.connect('cf_twitter.db')
    cursor = sqliteConnection.cursor()

    create_userConfig_table = f''' CREATE TABLE IF NOT EXISTS userConfig(
        rowid INTEGER PRIMARY KEY, user_handle TEXT, oauth_token TEXT, oauth_secret TEXT, consumer_key TEXT, consumer_sercret TEXT
    ); '''


if __name__ == '__main__':
    bot_handler = cf_bot_handler()
    app.run_server(debug=True) # For Hot Reloads
    #app.run_server() #Run Production Server
    #text LEADFPU to 33789, to virtually lead others to financial peace
    #Ken Coleman show, career clarity guide, free resource

    # business google search results optimizer: reputationdefender.com
