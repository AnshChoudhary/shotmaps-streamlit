import json
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

competitions_name = st.sidebar.selectbox("Select Competition",['La Liga', 'Champions League', 'Premier League'])
#seasons_name = st.sidebar.text_input("Enter the Season")
seasons_name = st.sidebar.selectbox("Select the Season", ['2019/2020', '2018/2019', '2017/2018', '2016/2017', '2015/2016', '2014/2015', '2013/2014', '2012/2013', '2011/2012', '2010/2011', '2009/2010', '2008/2009', '2007/2008', '2006/2007', '2005/2006', '2004/2005', '2003/2004', '2002/2003', '2001/2002', '2000/2001'])
home_team_required = st.sidebar.selectbox('Select Home Team', ["Barcelona","Real Madrid","Manchester United","Arsenal", "Liverpool","Chelsea","Juventus","AC Milan", "Atlético Madrid", "Manchester City","Tottenham Hotspur"])
away_team_required = st.sidebar.selectbox('Select Away Team', ["Barcelona","Real Madrid","Manchester United","Arsenal", "Liverpool","Chelsea","Juventus","AC Milan", "Atlético Madrid", "Manchester City","Tottenham Hotspur"])
state = st.sidebar.button("Get ShotMap!")


if state:
    with open('/Users/anshchoudhary/Desktop/SoccermaticsForPython-master/Statsbomb/data/competitions.json') as f:
        competitions = json.load(f)


    for competition in competitions:
        comp_name = competition['competition_name']
        if comp_name == competitions_name:
            competition_required_id = competition['competition_id']


    competition_id = competition_required_id

    # Initialize season_id
    for competition in competitions:
        season_name = competition['season_name']
        if season_name == seasons_name:
            season_required_id = competition['season_id']
    
    season_id = season_required_id

    with open('/Users/anshchoudhary/Desktop/SoccermaticsForPython-master/Statsbomb/data/matches/'+str(competition_id)+'/'+ str(season_id) +'.json') as f:
        matches = json.load(f)

   

    for match in matches:
        home_team_name=match['home_team']['home_team_name']
        away_team_name=match['away_team']['away_team_name']
        if (home_team_name==home_team_required) and (away_team_name==away_team_required):
            match_id_required = match['match_id']

    #Size of the pitch in yards (!!!)
    pitchLengthX=120
    pitchWidthY=80

    file_name=str(match_id_required)+'.json'

    with open('/Users/anshchoudhary/Desktop/SoccermaticsForPython-master/Statsbomb/data/events/'+file_name) as data_file:
        #print (mypath+'events/'+file)
        data = json.load(data_file)

    #get the nested structure into a dataframe 
    #store the dataframe in a dictionary with the match id as key (remove '.json' from string)
    from pandas import json_normalize
    df = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])


    #A dataframe of shots
    shots = df.loc[df['type_name'] == 'Shot'].set_index('id')
        
    #Draw the pitch
    from FCPython import createPitch
    (fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')

    #Plot the shots
    for i,shot in shots.iterrows():
        x=shot['location'][0]
        y=shot['location'][1]
        
        goal=shot['shot_outcome_name']=='Goal'
        team_name=shot['team_name']
        
        circleSize=2
        circleSize=np.sqrt(shot['shot_statsbomb_xg'])*5

        if (team_name==home_team_required):
            if goal:
                shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")
                shotCircle.set_alpha(.6)
                plt.text((x+1),pitchWidthY-y+1,shot['player_name']) 
            else:
                shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
                shotCircle.set_alpha(.2)
        elif (team_name==away_team_required):
            if goal:
                shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue")
                shotCircle.set_alpha(.6)
                plt.text((pitchLengthX-x+1),y+1,shot['player_name']) 
            else:
                shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue")      
                shotCircle.set_alpha(.2)
        ax.add_patch(shotCircle)
        
        
    plt.text(5,75,away_team_required + ' shots') 
    plt.text(80,75,home_team_required + ' shots') 
        
    fig.set_size_inches(10, 7)
    fig.savefig('Output/shots.jpeg', dpi=100) 

    st.header('Shotmap for the match between ' + home_team_required + " and " + away_team_required + " in the "+ seasons_name + " season")

    st.image('Output/shots.jpeg')