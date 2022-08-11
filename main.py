import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
#data from April 1, 2021 - October 3, 2021
mydata= pd.read_csv(r'C:\Users\micha\Desktop\savant_data.csv')

#block of code to convert pitch types into just "fastballs" or "offspeed"
pitch_type_series = mydata["pitch_type"]
pitch_type_list = pitch_type_series.tolist()
for i in range(len(pitch_type_list)):
  if pitch_type_list[i] == "FF" or pitch_type_list[i]=="SI" or pitch_type_list=="FT":
    pitch_type_list[i] = "fastball"
  else: pitch_type_list[i] = "offspeed"

#update the dataframe with this new pitch_type_list
mydata["type_of_pitch"] = pitch_type_list

#block of code to convert player names from "Judge, Aaron" to "Aaron Judge"
mydata["firstname"] = mydata.player_name.str.extract(r'\b(\w+)$',expand = True)  #using "regular expressions"
mydata["lastname"] = mydata.player_name.str.extract(r'\b(\w+)*', expand=True)   #using "regular expressions"
mydata["playername"] = mydata["firstname"] + " " + mydata["lastname"]

#If the "event" is something weird like a force_out,grounded_into_double_play, field_error, double_play, fielders_choice,
#(cont'd) fielders_choice_out, sac_fly_double_play,triple_play,catcher_interference, sac_bunt_double_play 
#(cont'd) then change the "event" to "field out"
mydata.loc[mydata["events"] == "force_out", "events"] = "field_out"
mydata.loc[mydata["events"] == "grounded_into_double_play", "events"] = "field_out"
mydata.loc[mydata["events"] == "field_error", "events"] = "field_out"
mydata.loc[mydata["events"] == "double_play", "events"] = "field_out"
mydata.loc[mydata["events"] == "fielders_choice", "events"] = "field_out"
mydata.loc[mydata["events"] == "fielders_choice_out", "events"] = "field_out"
mydata.loc[mydata["events"] == "sac_fly_double_play", "events"] = "field_out"
mydata.loc[mydata["events"] == "triple_play", "events"] = "field_out"
mydata.loc[mydata["events"] == "catcher_interf", "events"] = "field_out"
mydata.loc[mydata["events"] == "sac_bunt_double_play", "events"] = "field_out"
mydata.loc[mydata["events"] == "sac_fly", "events"] = "field_out"
mydata.loc[mydata["events"] == "sac_bunt", "events"] = "field_out"

mydata.loc[mydata["zone"] == 1.0, "zone"] = "high and left"
mydata.loc[mydata["zone"] == 2.0, "zone"] = "high and middle"
mydata.loc[mydata["zone"] == 3.0, "zone"] = "high and right"
mydata.loc[mydata["zone"] == 4.0, "zone"] = "middle and left"
mydata.loc[mydata["zone"] == 5.0, "zone"] = "down the middle"
mydata.loc[mydata["zone"] == 6.0, "zone"] = "middle and right"
mydata.loc[mydata["zone"] == 7.0, "zone"] = "low and left"
mydata.loc[mydata["zone"] == 8.0, "zone"] = "low and middle"
mydata.loc[mydata["zone"] == 9.0, "zone"] = "low and right"
mydata.loc[mydata["zone"] == 11.0, "zone"] = "high and left (ball)"
mydata.loc[mydata["zone"] == 12.0, "zone"] = "high and right (ball)"
mydata.loc[mydata["zone"] == 13.0, "zone"] = "low and left (ball)"
mydata.loc[mydata["zone"] == 14.0, "zone"] = "low and right (ball)"

#narrow down our dataframe into the columns that we're maybe gonna use
columns_used = ["type_of_pitch", "playername","events","description","zone","stand","p_throws","bat_score","fld_score"]
ourdata = mydata[columns_used]

#narrow down our dataframe to one where it's only balls hit into play (across all of MLB, all of 2021)
balls_in_play = ourdata["description"] == "hit_into_play"
our_df = ourdata[balls_in_play]

#dataframe where its only fastballs hit into play (across all of MLB, all of 2021)
fastballs = our_df["type_of_pitch"] == "fastball"
MLB_fastball_df = our_df[fastballs]

#dataframe where its only offspeed hit into play (across all of MLB, all of 2021) 
offspeed = our_df["type_of_pitch"] == "offspeed"
MLB_offspeed_df = our_df[offspeed]

#Calulcate league-wide stats
league_fieldout_fb = (MLB_fastball_df["events"].values=='field_out').sum()
league_single_fb = (MLB_fastball_df["events"].values=='single').sum()
league_double_fb = (MLB_fastball_df["events"].values=='double').sum()
league_triple_fb = (MLB_fastball_df["events"].values=='triple').sum()
league_homerun_fb = (MLB_fastball_df["events"].values=='home_run').sum()
league_all_fb = (MLB_fastball_df["events"].values!='').sum()

league_fieldout_percentage_fb = league_fieldout_fb / league_all_fb
league_single_percentage_fb = league_single_fb / league_all_fb
league_double_percentage_fb = league_double_fb / league_all_fb
league_triple_percentage_fb = league_triple_fb / league_all_fb
league_homerun_percentage_fb = league_homerun_fb / league_all_fb

league_fieldout_offspeed = (MLB_offspeed_df["events"].values=='field_out').sum()
league_single_offspeed = (MLB_offspeed_df["events"].values=='single').sum()
league_double_offspeed = (MLB_offspeed_df["events"].values=='double').sum()
league_triple_offspeed = (MLB_offspeed_df["events"].values=='triple').sum()
league_homerun_offspeed = (MLB_offspeed_df["events"].values=='home_run').sum()
league_all_offspeed = (MLB_offspeed_df["events"].values!='').sum()

league_fieldout_percentage_offspeed = league_fieldout_offspeed / league_all_offspeed
league_single_percentage_offspeed = league_single_offspeed / league_all_offspeed
league_double_percentage_offspeed = league_double_offspeed / league_all_offspeed
league_triple_percentage_offspeed = league_triple_offspeed / league_all_offspeed
league_homerun_percentage_offspeed = league_homerun_offspeed / league_all_offspeed

def scouting_report(name, pitcher_handedness):
  print("This is the scouting report for " + name, end=".\n\n")

  if pitcher_handedness == "R":
    throws = "against right-handed pitchers"
  elif pitcher_handedness == "L":
    throws = "against left-handed pitchers"
  
  print("Here is some relevant information about how " + name + " fares " + throws, end=".\n\n")
  
  #First, obtain the player's individual date frame
  player = mydata["playername"] == name
  player_df = mydata[player]
  player_df = player_df[player_df["p_throws"] == pitcher_handedness]

  player_bip = player_df["description"] == "hit_into_play"  ##bip stands for ball in play
  player_bip_df = player_df[player_bip]

  player_fastballs = player_bip_df["type_of_pitch"] == "fastball"
  player_fastballs_df = player_bip_df[player_fastballs]

  player_offspeed = player_bip_df["type_of_pitch"] == "offspeed"
  player_offspeed_df = player_bip_df[player_offspeed]

  #Next, calculate the player's individual statistics
  player_fieldout_fb = (player_fastballs_df["events"].values=='field_out').sum()
  player_single_fb = (player_fastballs_df["events"].values=='single').sum()
  player_double_fb = (player_fastballs_df["events"].values=='double').sum()
  player_triple_fb = (player_fastballs_df["events"].values=='triple').sum()
  player_homerun_fb = (player_fastballs_df["events"].values=='home_run').sum()
  player_all_fb = (player_fastballs_df["events"].values!='').sum()

  player_fieldout_percentage_fb = player_fieldout_fb / player_all_fb
  player_single_percentage_fb = player_single_fb / player_all_fb
  player_double_percentage_fb = player_double_fb / player_all_fb
  player_triple_percentage_fb = player_triple_fb / player_all_fb
  player_homerun_percentage_fb = player_homerun_fb / player_all_fb

  player_fieldout_offspeed = (player_offspeed_df["events"].values=='field_out').sum()
  player_single_offspeed = (player_offspeed_df["events"].values=='single').sum()
  player_double_offspeed = (player_offspeed_df["events"].values=='double').sum()
  player_triple_offspeed = (player_offspeed_df["events"].values=='triple').sum()
  player_homerun_offspeed = (player_offspeed_df["events"].values=='home_run').sum()
  player_all_offspeed = (player_offspeed_df["events"].values!='').sum()

  player_fieldout_percentage_offspeed = player_fieldout_offspeed / player_all_offspeed
  player_single_percentage_offspeed = player_single_offspeed / player_all_offspeed
  player_double_percentage_offspeed = player_double_offspeed / player_all_offspeed
  player_triple_percentage_offspeed = player_triple_offspeed / player_all_offspeed
  player_homerun_percentage_offspeed = player_homerun_offspeed / player_all_offspeed

  #Finally, print out the comparisons between a player's individual statistics and the league-wide statistics
  if abs(player_single_percentage_fb - league_single_percentage_fb) > 0.03:
    print(name, "hits fastballs for singles", throws, format(player_single_percentage_fb,".0%"), "of the time, while the league hits them", format(league_single_percentage_fb,".0%"), "of the time")
  if abs(player_double_percentage_fb - league_double_percentage_fb) > 0.03:
    print(name, "hits fastballs for doubles", throws, format(player_double_percentage_fb,".0%"), "of the time, while the league hits them", format(league_double_percentage_fb,".0%"), "of the time")
  if abs(player_triple_percentage_fb - league_triple_percentage_fb) > 0.03:
    print(name, "hits fastballs for triples", throws, format(player_triple_percentage_fb,".0%"), "of the time, while the league hits them", format(league_triple_percentage_fb,".0%"), "of the time")
  if abs(player_homerun_percentage_fb - league_homerun_percentage_fb) > 0.03:
    print(name, "hits fastballs for home runs", throws, format(player_homerun_percentage_fb,".0%"), "of the time, while the league hits them", format(league_homerun_percentage_fb,".0%"), "of the time")
  if abs(player_fieldout_percentage_fb - league_fieldout_percentage_fb) > 0.03:
    print(name, "hits fastballs for outs", throws, format(player_fieldout_percentage_fb,".0%"), "of the time, while the league hits them", format(league_fieldout_percentage_fb,".0%"), "of the time")
  print("")
  if abs(player_single_percentage_offspeed - league_single_percentage_offspeed) > 0.03:
    print(name, "hits offspeed pitches for singles", throws, format(player_single_percentage_offspeed,".0%"), "of the time, while the league hits them", format(league_single_percentage_offspeed,".0%"), "of the time")
  if abs(player_double_percentage_offspeed - league_double_percentage_offspeed) > 0.03:
    print(name, "hits offspeed pitches for doubles", throws, format(player_double_percentage_offspeed,".0%"), "of the time, while the league hits them", format(league_double_percentage_offspeed,".0%"), "of the time")
  if abs(player_triple_percentage_offspeed - league_triple_percentage_offspeed) > 0.03:
    print(name, "hits offspeed pitches for triples", throws, format(player_triple_percentage_offspeed,".0%"), "of the time, while the league hits them", format(league_triple_percentage_offspeed,".0%"), "of the time")
  if abs(player_homerun_percentage_offspeed - league_homerun_percentage_offspeed) > 0.03:
    print(name, "hits offspeed pitches for home runs", throws, format(player_homerun_percentage_offspeed,".0%"), "of the time, while the league hits them", format(league_homerun_percentage_offspeed,".0%"), "of the time")
  if abs(player_fieldout_percentage_offspeed - league_fieldout_percentage_offspeed) > 0.03:
    print(name, "hits offspeed pitches for outs", throws, format(player_fieldout_percentage_offspeed,".0%"), "of the time, while the league hits them", format(league_fieldout_percentage_offspeed,".0%"), "of the time")
  print("")

def charts_fastball(name, pitcher_handedness):
  player = mydata["playername"] == name
  player_df = mydata[player]
  player_df = player_df[player_df["p_throws"] == pitcher_handedness]

  player_bip = player_df["description"] == "hit_into_play"  ##bip stands for ball in play
  player_bip_df = player_df[player_bip]

  player_fastballs = player_bip_df["type_of_pitch"] == "fastball"
  player_fastballs_df = player_bip_df[player_fastballs]

#pie charts:
  player_fastballs_events_df = player_fastballs_df["events"].value_counts() #renamed the dataframe
  player_fastballs_events_df.plot(x=[[0]], y=[[1]], kind ="pie",autopct='%1.1f%%',title="Player's Results on Fastballs Hit into Play")

def charts_offspeed(name, pitcher_handedness):
  player = mydata["playername"] == name
  player_df = mydata[player]
  player_df = player_df[player_df["p_throws"] == pitcher_handedness]

  player_bip = player_df["description"] == "hit_into_play"  ##bip stands for ball in play
  player_bip_df = player_df[player_bip]

  player_offspeed = player_bip_df["type_of_pitch"] == "offspeed"
  player_offspeed_df = player_bip_df[player_offspeed]
#pie charts:
  player_offspeed_events_df = player_offspeed_df["events"].value_counts()
  player_offspeed_events_df.plot(x=[[0]], y=[[1]], kind ="pie",autopct='%1.1f%%', title="Player's Results on Offspeed Pitches Hit into Play")


def heat_map_fastball(name, pitcher_handedness):
  graph_columns_fastball = ["playername","events","zone","p_throws","type_of_pitch"] #Narrow data down to columns we will use for graph
  graph_df_fastball = our_df[graph_columns_fastball] #Set new dataframe with only the three categories above
  graph_df_fastball = graph_df_fastball[graph_df_fastball['playername'] == name]
  graph_df_fastball = graph_df_fastball[graph_df_fastball['p_throws'] == pitcher_handedness]
  graph_df_fastball = graph_df_fastball[graph_df_fastball["type_of_pitch"] == "fastball"]

  graph_df_fastball.groupby('events').zone.value_counts() #Group events and categorize by zone

  zone_events_fastball = (graph_df_fastball #Set variable for heatmap and create grid format
    .groupby('events')
    .zone
    .value_counts()
    .unstack()
    .fillna(0)
    )

  fig, ax = plt.subplots()
  plt.title("Player Heatmap: Fastballs")
  ax.set_ylim(1, 5)
  sns.heatmap(zone_events_fastball, cmap="Blues")
  plt.show()

#Offspeed Heatmap for Individual Player

def heat_map_offspeed(name, pitcher_handedness):
  graph_columns_df_offspeed = ["playername","events","zone","p_throws","type_of_pitch"] #Narrow data down to columns we will use for graph
  graph_df_offspeed = our_df[graph_columns_df_offspeed] #Set new dataframe with only the three categories above
  graph_df_offspeed = graph_df_offspeed[graph_df_offspeed['playername'] == name]
  graph_df_offspeed = graph_df_offspeed[graph_df_offspeed["type_of_pitch"] == "offspeed"]
  graph_df_offspeed = graph_df_offspeed[graph_df_offspeed['p_throws'] == pitcher_handedness]

  graph_df_offspeed.groupby('events').zone.value_counts() #Group events and categorize by zone

  zone_events_offspeed = (graph_df_offspeed #Set variable for heatmap and create grid format
   .groupby('events')
   .zone
   .value_counts()
   .unstack()
   .fillna(0)
   )

  fig, ax = plt.subplots()
  plt.title("Player Heatmap: Offspeed")
  ax.set_ylim(1, 5)
  sns.heatmap(zone_events_offspeed, cmap="Blues")
  plt.show()

#Final Product - Input Boxes

def baseball_analysis(name, pitcher_handedness):
  scouting_report(name, pitcher_handedness)
  charts_fastball(name, pitcher_handedness)
  heat_map_fastball(name, pitcher_handedness)

pick_a_player = input("Who do you want a scouting report of? ")
pitcher_handedness = input("Is the opposing pitcher a righty or a lefty? Enter 'R' or 'L': ")
baseball_analysis(pick_a_player, pitcher_handedness)

answer_to_question = input("Would you like to see offspeed data for " + pick_a_player + "? Input yes or no: ")
if answer_to_question.lower() == "yes":
  charts_offspeed(pick_a_player, pitcher_handedness)
  heat_map_offspeed(pick_a_player, pitcher_handedness)

print("Hello!")