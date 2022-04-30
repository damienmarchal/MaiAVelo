# Deployement workflow from github
#  0) copy the file config.json in your working directory
#     fill the config.json file with valid id&password and website adresse.
#  1) call data-update to:
#     - prepare all the data using private and public data, everything is stored in dedicated directory called database
#     - copy the website structure to the webserver
#     - copy the computed data to the webserver

out_db="../database"                #< where the generated file will be
out_website="../website"            #< where the generated site will be
config_file="../config.json"        #< where the deployement private information will be
public_src_db="crowdsourced-data"   #< where the crowdsourced data will be (the invite & url infos)

# convert xls to json, drop private column and normalize column naming,
python3 re-format-data-from-xls.py $1 ${out_db}/latest-data-step1.json

# add the invitation links into the existing file
python3 add-invite-url.py ${out_db}/latest-data-step1.json ${public_src_db}/invitation-links.json ${out_db}/latest-data-step2.json

# add historical data in team size progression
python3 add-recent-progress.py ${out_db}/latest-data-step2.json ${out_db}/latest-data-step2.json ${out_db}/latest-data.json

# compute the regional statistics
python3 make-stats.py city ${out_db}/latest-data.json ${out_db}/latest-stats-city.json
python3 make-stats.py epci ${out_db}/latest-data.json ${out_db}/latest-stats-epci.json
python3 make-stats.py department ${out_db}/latest-data.json ${out_db}/latest-stats-department.json
python3 make-stats.py region ${out_db}/latest-data.json ${out_db}/latest-stats-region.json

# start from a fresh site
rm -rf ${out_website}
cp -rf website ${out_website}
cp ${out_db}/latest-data.json ${out_website}/ChallengeMaiAVelo2022/database/data.json
cp ${out_db}/latest-stats-city.json ${out_website}/ChallengeMaiAVelo2022/database/stats-city.json
cp ${out_db}/latest-stats-epci.json ${out_website}/ChallengeMaiAVelo2022/database/stats-epci.json
cp ${out_db}/latest-stats-department.json ${out_website}/ChallengeMaiAVelo2022/database/stats-department.json
cp ${out_db}/latest-stats-region.json ${out_website}/ChallengeMaiAVelo2022/database/stats-region.json

# when ready ... publish now
# python3 publish-website.py ${config_file} ${out_website}
