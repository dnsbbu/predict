# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd;


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_date', methods=['GET'])
def get_date():
    selected_date = request.args.get('date')
    file_path =f"/var/www/html/Horsestaticwinn/{selected_date}.csv"
    try:
        data1 = pd.read_csv(file_path)
        venue_options = data1['venueName'].unique()
        return jsonify({'venues': venue_options.tolist()})
    except FileNotFoundError:
        return jsonify({'error': f'CSV file for date {selected_date} not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_race',methods=['GET'])
def get_race():
    selected_venue=request.args.get('venue')
    selected_date = request.args.get('date')
    file_path =f"/var/www/html/Horsestaticwinn/{selected_date}.csv"
    try:
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        Race_options = racedata['race_no'].unique()
        return jsonify({'races': Race_options.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/getpredictvenue',methods=['GET'])
def getpredictvenue():

    predictedvenues=pd.read_csv("/var/www/html/Horsestaticwinn/Venues.csv")
    predictedvenuess=predictedvenues['venueName']
    return jsonify({'predictedvenuess': predictedvenuess.tolist()})


@app.route('/getpre',methods=['GET'])
def getpre():
    selected_venue=request.args.get('selected_venue')
    formatted_date = request.args.get('formatted_date')
    selected_Race=request.args.get('selected_Race')
    selectedpredict_venue=request.args.get('selectedpredict_venue')
    if(selectedpredict_venue=='All'):
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        # file_path =f"/var/www/html/Horsestaticwinn/{formatted_date}.csv"
        # data1 = pd.read_csv(file_path)
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        for row in data_list:
            total = len(df[(df['jockey_id'] == row['jockey_id'])])
            first_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 1)])
            second_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 2)])
            third_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['jockey_id'] == row['jockey_id']) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    else:
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 1) ])
            second_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 2)])
            third_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Venue':selectedpredict_venue,
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    return jsonify({'predictedvenuess': data})

@app.route('/gettrainer',methods=['GET'])
def gettrainer():
    selected_venue=request.args.get('selected_venue')
    formatted_date = request.args.get('formatted_date')
    selected_Race=request.args.get('selected_Race')
    selectedpredict_venue=request.args.get('selectedpredict_venue')
    if(selectedpredict_venue=='All'):
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['trainer_id'] == row['trainer_id'])])
            first_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 1)])
            second_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 2)])
            third_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['trainer_id'] == row['trainer_id']) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    else:
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 1) ])
            second_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 2)])
            third_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Venue':selectedpredict_venue,
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    
    return jsonify({'predictedvenuess': data})

@app.route('/gethorse',methods=['GET'])
def gethorse():
    selected_venue=request.args.get('selected_venue')
    formatted_date = request.args.get('formatted_date')
    selected_Race=request.args.get('selected_Race')
    selectedpredict_venue=request.args.get('selectedpredict_venue')
    if(selectedpredict_venue=='All'):
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            # print(row['horse_id'])
            total = len(df[(df['horse_id'] == row['horse_id'])])
            first_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 1)])
            second_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 2)])
            third_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['horse_id'] == row['horse_id']) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    else:
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 1) ])
            second_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 2)])
            third_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Venue':selectedpredict_venue,
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    return jsonify({'predictedvenuess': data})
@app.route('/getsire',methods=['GET'])
def getsire():
    selected_venue=request.args.get('selected_venue')
    formatted_date = request.args.get('formatted_date')
    selected_Race=request.args.get('selected_Race')
    selectedpredict_venue=request.args.get('selectedpredict_venue')
    if(selectedpredict_venue=='All'):
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            # print(row['sireId'])
            total = len(df[(df['sireId'] == row['sireId'])])
            # print(df[(df['horse_id'] == row['sireId'])])
            first_place_count = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 1)])
            second_place_count = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 2)])
            third_place_count = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['sireId'] == row['sireId']) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Sire_Name':row['sireName'],
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    else:
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 1) ])
            second_place_count = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 2)])
            third_place_count = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Sire_Name':row['sireName'],
                'Venue':selectedpredict_venue,
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    return jsonify({'predictedvenuess': data})

@app.route('/getdam',methods=['GET'])
def getdam():
    selected_venue=request.args.get('selected_venue')
    formatted_date = request.args.get('formatted_date')
    selected_Race=request.args.get('selected_Race')
    selectedpredict_venue=request.args.get('selectedpredict_venue')
    if(selectedpredict_venue=='All'):
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['damId'] == row['damId'])])
            first_place_count = len(df[(df['damId'] == row['damId']) & (df['place'] == 1)])
            second_place_count = len(df[(df['damId'] == row['damId']) & (df['place'] == 2)])
            third_place_count = len(df[(df['damId'] == row['damId']) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['damId'] == row['damId']) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['damId'] == row['damId']) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['damId'] == row['damId']) & (df['place'] == 6)])
            # print((round((first_place_count / total) * 100, 2)))
            sixth_above_place_count = len(df[ (df['damId'] == row['damId']) & (df['place'] > 6)])
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Dam_Name':row['damName'],
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    else:
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 1) ])
            second_place_count = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 2)])
            third_place_count = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] > 6)])
            # print((round((first_place_count / total) * 100, 2)))
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Dam_Name':row['damName'],
                'Venue':selectedpredict_venue,
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format(round((first_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Second_Place_Percentage': '{:.2f}'.format(round((second_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Third_Place_Percentage':  '{:.2f}'.format(round((third_place_count / total) * 100, 2))if total > 0 else '0.00',
                'Fourth_Place_Percentage':  '{:.2f}'.format(round((fourth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Fifth_Place_Percentage':  '{:.2f}'.format(round((fifth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_place_count / total) * 100, 2)) if total > 0 else '0.00',
                'Above_Sixth_Place_Percentage':  '{:.2f}'.format(round((sixth_above_place_count / total) * 100, 2)) if total > 0 else '0.00'
            }
            data.append(class_data)
    return jsonify({'predictedvenuess': data})

@app.route('/gettotalpercentage',methods=['GET'])
def gettotalpercentage():
    selected_venue=request.args.get('selected_venue')
    formatted_date = request.args.get('formatted_date')
    selected_Race=request.args.get('selected_Race')
    selectedpredict_venue=request.args.get('selectedpredict_venue')
    if(selectedpredict_venue=='All'):
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        for row in data_list:

            # jockey 
            total = len(df[(df['jockey_id'] == row['jockey_id'])])
            first_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 1)])
            second_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 2)])
            third_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 3)])
            fourth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 4)])
            fifth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 5)])
            sixth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 6)])
            sixth_above_place_count = len(df[ (df['jockey_id'] == row['jockey_id']) & (df['place'] > 6)])

            #trainer
            total1 = len(df[(df['trainer_id'] == row['trainer_id'])])
            first_place_count1 = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 1)])
            second_place_count1 = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 2)])
            third_place_count1= len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 3)])
            fourth_place_count1 = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 4)])
            fifth_place_count1= len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 5)])
            sixth_place_count1= len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 6)])
            sixth_above_place_count1 = len(df[ (df['trainer_id'] == row['trainer_id']) & (df['place'] > 6)])

            # horse
            total2 = len(df[(df['horse_id'] == row['horse_id'])])
            first_place_count2 = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 1)])
            second_place_count2 = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 2)])
            third_place_count2= len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 3)])
            fourth_place_count2 = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 4)])
            fifth_place_count2= len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 5)])
            sixth_place_count2= len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 6)])
            sixth_above_place_count2 = len(df[ (df['horse_id'] == row['horse_id']) & (df['place'] > 6)])


            #sire
            total3 = len(df[(df['sireId'] == row['sireId'])])
            # print(df[(df['horse_id'] == row['sireId'])])
            first_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 1)])
            second_place_count3 = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 2)])
            third_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 3)])
            fourth_place_count3 = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 4)])
            fifth_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 5)])
            sixth_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 6)])
            sixth_above_place_count3 = len(df[ (df['sireId'] == row['sireId']) & (df['place'] > 6)])

            #dam
            total4 = len(df[(df['damId'] == row['damId'])])
            first_place_count4= len(df[(df['damId'] == row['damId']) & (df['place'] == 1)])
            second_place_count4 = len(df[(df['damId'] == row['damId']) & (df['place'] == 2)])
            third_place_count4= len(df[(df['damId'] == row['damId']) & (df['place'] == 3)])
            fourth_place_count4 = len(df[(df['damId'] == row['damId']) & (df['place'] == 4)])
            fifth_place_count4= len(df[(df['damId'] == row['damId']) & (df['place'] == 5)])
            sixth_place_count4= len(df[(df['damId'] == row['damId']) & (df['place'] == 6)])
            sixth_above_place_count4 = len(df[ (df['damId'] == row['damId']) & (df['place'] > 6)])
            # First_Place_Percentage=(round((first_place_count/total) * 100, 2)if total != 0 else 0)+(round((first_place_count1 / total1) * 100, 2) if total1 != 0 else 0)+(round((first_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
            # +(round((first_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((first_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
        
            # # print((round((first_place_count/total) * 100, 2)if total != 0 else 0)+(round((first_place_count1 / total1) * 100, 2) if total1 != 0 else 0)+(round((first_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
            # # +(round((first_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((first_place_count4 / total4) * 100, 2)if total4 != 0 else 0))
            # Second_Place_Percentage=(round((second_place_count / total) * 100, 2)if total != 0 else 0)+(round((second_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((second_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +round((second_place_count3 / total3) * 100, 2)+round((second_place_count4 / total4) * 100, 2)
            
            # Third_Place_Percentage=(round((third_place_count / total) * 100, 2)if total != 0 else 0)+(round((third_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((third_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
            # +(round((third_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((third_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
           
            # Fourth_Place_Percentage=(round((fourth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fourth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fourth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +(round((fourth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fourth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            
            # Fifth_Place_Percentage=(round((fifth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fifth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fifth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +(round((fifth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fifth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            
            # Sixth_Place_Percentage=(round((sixth_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((sixth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +(round((sixth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            
            # Above_Sixth_Place_Percentage=(round((sixth_above_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_above_place_count1 / total1) * 100, 2)if total1 != 0 else 0)
            # +(round((sixth_above_place_count2 / total2) * 100, 2)if total2 != 0 else 0)+(round((sixth_above_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_above_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format((round((first_place_count/total) * 100, 2)if total != 0 else 0)+(round((first_place_count1 / total1) * 100, 2) if total1 != 0 else 0)+(round((first_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
                 +(round((first_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((first_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Second_Place_Percentage': '{:.2f}'.format((round((second_place_count / total) * 100, 2)if total != 0 else 0)+(round((second_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((second_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
                +round((second_place_count3 / total3) * 100, 2)+(round((second_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Third_Place_Percentage': '{:.2f}'.format((round((third_place_count / total) * 100, 2)if total != 0 else 0)+(round((third_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((third_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
                +(round((third_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((third_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Fourth_Place_Percentage':  '{:.2f}'.format((round((fourth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fourth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fourth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
                +(round((fourth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fourth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Fifth_Place_Percentage':'{:.2f}'.format((round((fifth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fifth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fifth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
               +(round((fifth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fifth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Sixth_Place_Percentage': '{:.2f}'.format((round((sixth_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((sixth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
               +(round((sixth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Above_Sixth_Place_Percentage':'{:.2f}'.format((round((sixth_above_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_above_place_count1 / total1) * 100, 2)if total1 != 0 else 0)
               +(round((sixth_above_place_count2 / total2) * 100, 2)if total2 != 0 else 0)+(round((sixth_above_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_above_place_count4 / total4) * 100, 2)if total4 != 0 else 0))
            }
            data.append(class_data)
    else:
        data=[]
        df=pd.read_csv("/home/sumanth/Desktop/Flaskpro/application/full1.csv")
        file_path =f"/home/sumanth/Desktop/Flaskpro/application/{formatted_date}.csv"
        data1 = pd.read_csv(file_path)
        racedata=data1[data1['venueName']==selected_venue]
        filtered_data = racedata[racedata['race_no']==selected_Race]
        data_list = filtered_data.to_dict('records')
        # print(len(data_list))
        for row in data_list:
            total = len(df[(df['jockey_id'] == row['jockey_id']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 1) & (df['venueName'] == selectedpredict_venue)])
            second_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 2) & (df['venueName'] == selectedpredict_venue)])
            third_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 3) & (df['venueName'] == selectedpredict_venue)])
            fourth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 4) & (df['venueName'] == selectedpredict_venue)])
            fifth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 5) & (df['venueName'] == selectedpredict_venue)])
            sixth_place_count = len(df[(df['jockey_id'] == row['jockey_id']) & (df['place'] == 6) & (df['venueName'] == selectedpredict_venue)])
            sixth_above_place_count = len(df[ (df['jockey_id'] == row['jockey_id']) & (df['place'] > 6) & (df['venueName'] == selectedpredict_venue)])

            #trainer
            total1 = len(df[(df['trainer_id'] == row['trainer_id']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count1 = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 1) & (df['venueName'] == selectedpredict_venue)])
            second_place_count1 = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 2)& (df['venueName'] == selectedpredict_venue)])
            third_place_count1= len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 3) & (df['venueName'] == selectedpredict_venue)])
            fourth_place_count1 = len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 4)& (df['venueName'] == selectedpredict_venue)])
            fifth_place_count1= len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 5)& (df['venueName'] == selectedpredict_venue)])
            sixth_place_count1= len(df[(df['trainer_id'] == row['trainer_id']) & (df['place'] == 6)& (df['venueName'] == selectedpredict_venue)])
            sixth_above_place_count1 = len(df[ (df['trainer_id'] == row['trainer_id']) & (df['place'] > 6) & (df['venueName'] == selectedpredict_venue)])

            # horse
            total2 = len(df[(df['horse_id'] == row['horse_id']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count2 = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 1) & (df['venueName'] == selectedpredict_venue)])
            second_place_count2 = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 2)& (df['venueName'] == selectedpredict_venue)])
            third_place_count2= len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 3) & (df['venueName'] == selectedpredict_venue)])
            fourth_place_count2 = len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 4) & (df['venueName'] == selectedpredict_venue)])
            fifth_place_count2= len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 5) & (df['venueName'] == selectedpredict_venue)])
            sixth_place_count2= len(df[(df['horse_id'] == row['horse_id']) & (df['place'] == 6) & (df['venueName'] == selectedpredict_venue)])
            sixth_above_place_count2 = len(df[ (df['horse_id'] == row['horse_id']) & (df['place'] > 6) & (df['venueName'] == selectedpredict_venue)])


            #sire
            total3 = len(df[(df['sireId'] == row['sireId']) & (df['venueName'] == selectedpredict_venue)])
            # print(df[(df['horse_id'] == row['sireId'])])
            first_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 1) & (df['venueName'] == selectedpredict_venue)])
            second_place_count3 = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 2) & (df['venueName'] == selectedpredict_venue)])
            third_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 3) & (df['venueName'] == selectedpredict_venue)])
            fourth_place_count3 = len(df[(df['sireId'] == row['sireId']) & (df['place'] == 4) & (df['venueName'] == selectedpredict_venue)])
            fifth_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 5) & (df['venueName'] == selectedpredict_venue)])
            sixth_place_count3= len(df[(df['sireId'] == row['sireId']) & (df['place'] == 6) & (df['venueName'] == selectedpredict_venue)])
            sixth_above_place_count3 = len(df[ (df['sireId'] == row['sireId']) & (df['place'] > 6) & (df['venueName'] == selectedpredict_venue)])

            #dam
            total4 = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue)])
            first_place_count4 = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 1) ])
            second_place_count4 = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 2)])
            third_place_count4 = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 3)])
            fourth_place_count4 = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 4)])
            fifth_place_count4 = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 5)])
            sixth_place_count4 = len(df[(df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] == 6)])
            sixth_above_place_count4 = len(df[ (df['damId'] == row['damId']) & (df['venueName'] == selectedpredict_venue) & (df['place'] > 6)])

            # First_Place_Percentage=(round((first_place_count/total) * 100, 2)if total != 0 else 0)+(round((first_place_count1 / total1) * 100, 2) if total1 != 0 else 0)+(round((first_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
            # +(round((first_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((first_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            # print((round((first_place_count/total) * 100, 2)if total != 0 else 0))
            # print((round((first_place_count1/total1) * 100, 2)if total1 != 0 else 0))
            # print((round((first_place_count2/total) * 100, 2)if total2 != 0 else 0))
            # print((round((first_place_count3/total) * 100, 2)if total3 != 0 else 0))
            # print((round((first_place_count4 / total4) * 100, 2)if total4 != 0 else 0))
            
            # Second_Place_Percentage=(round((second_place_count / total) * 100, 2)if total != 0 else 0)+(round((second_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((second_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +round((second_place_count3 / total3) * 100, 2)+round((second_place_count4 / total4) * 100, 2)
            
            # Third_Place_Percentage=(round((third_place_count / total) * 100, 2)if total != 0 else 0)+(round((third_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((third_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
            # +(round((third_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((third_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
           
            # Fourth_Place_Percentage=(round((fourth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fourth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fourth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +(round((fourth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fourth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            
            # Fifth_Place_Percentage=(round((fifth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fifth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fifth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +(round((fifth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fifth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            
            # Sixth_Place_Percentage=(round((sixth_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((sixth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
            # +(round((sixth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            
            # Above_Sixth_Place_Percentage=(round((sixth_above_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_above_place_count1 / total1) * 100, 2)if total1 != 0 else 0)
            # +(round((sixth_above_place_count2 / total2) * 100, 2)if total2 != 0 else 0)+(round((sixth_above_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_above_place_count4 / total4) * 100, 2)if total4 != 0 else 0)
            class_data = {
                'Horse_No':row['Horse_No'],
                'Horse_Name':row['horseName'],
                'Jockey_Name':row['jockeyName'],
                'Trainer_Name':row['trainerName'],
                'Total_Race_Participated':total,
                'First_Place_Percentage': '{:.2f}'.format((round((first_place_count/total) * 100, 2)if total != 0 else 0)+(round((first_place_count1 / total1) * 100, 2) if total1 != 0 else 0)+(round((first_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
                 +(round((first_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((first_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Second_Place_Percentage': '{:.2f}'.format((round((second_place_count / total) * 100, 2)if total != 0 else 0)+(round((second_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((second_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
                +round((second_place_count3 / total3) * 100, 2)+(round((second_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Third_Place_Percentage': '{:.2f}'.format((round((third_place_count / total) * 100, 2)if total != 0 else 0)+(round((third_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((third_place_count2 / total2) * 100, 2) if total2 != 0 else 0)
                +(round((third_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((third_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Fourth_Place_Percentage':  '{:.2f}'.format((round((fourth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fourth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fourth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
                +(round((fourth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fourth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Fifth_Place_Percentage':'{:.2f}'.format((round((fifth_place_count / total) * 100, 2)if total != 0 else 0)+(round((fifth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((fifth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
               +(round((fifth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((fifth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Sixth_Place_Percentage': '{:.2f}'.format((round((sixth_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_place_count1 / total1) * 100, 2)if total1 != 0 else 0)+(round((sixth_place_count2 / total2) * 100, 2)if total2 != 0 else 0)
               +(round((sixth_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_place_count4 / total4) * 100, 2)if total4 != 0 else 0)),
                'Above_Sixth_Place_Percentage':'{:.2f}'.format((round((sixth_above_place_count / total) * 100, 2)if total != 0 else 0)+(round((sixth_above_place_count1 / total1) * 100, 2)if total1 != 0 else 0)
               +(round((sixth_above_place_count2 / total2) * 100, 2)if total2 != 0 else 0)+(round((sixth_above_place_count3 / total3) * 100, 2)if total3 != 0 else 0)+(round((sixth_above_place_count4 / total4) * 100, 2)if total4 != 0 else 0))
            }
            data.append(class_data)
    return jsonify({'predictedvenuess': data})

if __name__ == '__main__':
    app.run(debug=True)
