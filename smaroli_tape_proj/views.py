'''
Created on Apr 30, 2018

@author: marol
'''
#import packages
from django.shortcuts import render
from twilio.rest import Client
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#handling initial page
def home(request):
    return render(request,'smaroli_tape_proj/form.html')

#handling final page
def final(request):
    try:
        #connect to spotify
        SPOTIPY_CLIENT_ID = '9b6d0f93e5f94463bc61e8b878206ae4'
        SPOTIPY_CLIENT_SECRET = '729a1b7e6a7f466aa2b83c2e906b59d5'
        client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        #connect to twilio
        TWILIO_ACCOUNT_SID = 'AC8c290ea0604844ed5dd99f2a2bd3bbf6'
        TWILIO_AUTH_TOKEN = '0b6d3183c861a11a5b0bb521650132d8'
        client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
        
        #get artist name
        artist_name = request.POST.get('artist_name')
        #pick top track of artist from spotify
        artist_results = spotify.search(q='artist:{}'.format(artist_name), type='artist', limit=1)
        artist = artist_results['artists']['items'][0]
        top_track_results = spotify.artist_top_tracks(artist['id'], country='US')
        top_track = top_track_results['tracks'][0]

        #text message body
        body_custom = "{}'s top track: {}".format(artist['name'], top_track['name'])
        body = body_custom
        from_ = "+17049097203"
        to = request.POST.get('phone_number')
        
        #send details to next page and send text message
        try:
            message = client.messages.create(body=body,to=to,from_=from_)
            args = {'identify':'Thank You! Top Track Details have been sent to your number :)',
                    'artist_name':artist['name'],
                    'artist_image':artist['images'][0]['url'],
                    'top_track':top_track['name'],
                    'followers':artist['followers']['total'],
                    'genres':artist['genres'],
                    'popularity':artist['popularity']
                    }
            return render(request,'smaroli_tape_proj/final.html',args)
        
        #catch exception from twilio
        except:
            args = {'identify':'Thank You! Due to Twilio restrictions SMS cannot be sent :(',
                    'artist_name':artist['name'],
                    'artist_image':artist['images'][0]['url'],
                    'top_track':top_track['name'],
                    'followers':artist['followers']['total'],
                    'genres':artist['genres'],
                    'popularity':artist['popularity']
                    }
            return render(request,'smaroli_tape_proj/final.html',args)
            
    #catch exception from spotify   
    except:
        args = {'identify':'Thank You! But artist Not Found. Please check your input :(',
                'artist_name':'Not Available',
                'artist_image':'Not Available',
                'top_track':'Not Available',
                'followers':'Not Available',
                'genres':'Not Available',
                'popularity':'Not Available'
        }
        return render(request,'smaroli_tape_proj/final.html',args)
   
        
