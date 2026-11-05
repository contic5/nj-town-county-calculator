import pandas as pd

def split_into_parts(line):
    max_spaces_streak=0
    spaces_streak=0
    for letter in line:
        if letter==" ":
            spaces_streak+=1
            max_spaces_streak=max(spaces_streak,max_spaces_streak)
        else:
            spaces_streak=0

    return line.split(" "*max_spaces_streak)

def main():
    town_arr=[]
    town_id=1

    county_arr=[]
    county_dict={"County":"TEST","Towns":0}
    county_id=1
    county=""
 
    with open("raw_county_text.txt") as target_file:
        lines=target_file.readlines()
        lines=[line.strip() for line in lines]

    line_index=0

    while line_index<len(lines):
        line=lines[line_index]

        #New County Started
        if " County" in line:
            county_dict={"County":line,"Towns":0}
            print(line)
            county=line
            line_index+=1
        #Line to Skip
        elif line=="" or line.count(" ")==0:
            line_index+=1
            if county_dict["Towns"]>0:
                county_arr.append(county_dict)
        #County Town
        else:
            parts=split_into_parts(line)
            if parts!=['Muncipality', 'Treasury']:
                print(parts)

                town_dict={"ID":town_id,"Town":parts[0].title(),"County":county,"Treasury Code":parts[1]}
                town_id+=1

                town_arr.append(town_dict)
                county_dict["Towns"]+=1

            line_index+=1

    county_arr.append(county_dict)

    town_df=pd.DataFrame.from_dict(town_arr)
    county_df=pd.DataFrame.from_dict(county_arr)

    print(town_df.head())
    print(county_df.head())

    with pd.ExcelWriter("NJ Towns by County.xlsx") as writer:
        town_df.to_excel(writer, sheet_name="Towns")
        county_df.to_excel(writer, sheet_name="Counties")

if __name__=="__main__":
    main()