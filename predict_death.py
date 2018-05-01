import seaborn as sns
sns.set(color_codes=True)
import pandas as pd

# Let's make a function for predicting the day of your death. Fun!!!
def predict_day_of_death(df, filters, plot_color, line_label):
        
    for cat,val in filters:
        df = df[df[cat]==val]
    
    # run kernel density estimation and plot it
    try:
        h = sns.kdeplot(df.detail_age.astype('int32'), shade=True, label=line_label, color=plot_color, cut=0)
    except ZeroDivisionError:
        print 'Oops, number of records is ' + str(len(df))
        return  
    
    # extract line info
    xy = h.get_lines()[len(h.get_lines())-1].get_data()
    # get day of death
    dod = max(enumerate(xy[1]), key=(lambda x: x[1]))
    day_of_death = xy[0][int(dod[0])]
    
    # autoscale plot
    h.autoscale(enable=True)
    
    print '{0} will most likely die at {1} years old.'.format(line_label, day_of_death)
    
    return day_of_death


def death_date_over_years(years, cols, filt, demographic):
    death_dates=[];
    
    for year in years:
        # load
        df = pd.read_csv('~/Desktop/mortality/'+str(year)+'_data.csv', usecols=cols, dtype=object)
        # clean up 
        if 'education_reporting_flag' in cols:
            df = df[df.education_reporting_flag=='1']
        df = df[df.detail_age_type=='1']  
        df = df[df.detail_age!='999']

        x = predict_day_of_death(df, filt, 'k', demographic)
        death_dates.append(x)
    
    return death_dates