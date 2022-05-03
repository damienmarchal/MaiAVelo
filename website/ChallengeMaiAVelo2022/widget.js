const URL = "./widgets/teams/";

/// change value of a numeric fields with an animation changing
/// progressively the value from previous one to new one.
function setNewValue(target, currentValue, newValue, formatter)
{
  /// We can now start animating things
  $(target).prop('Counter', currentValue).animate({
    Counter: newValue
  },{
    duration: 1000,
    easing: 'swing',
    step: function (value)
    {
      $(this).text(formatter(value));
    }
  });
}

/// Return the html line for one of the team entry.
function getHtmlForTeamEntry(name, id, withDetails)
{
  entry = `<div class="col-sm"><ul><li> ${name}`
  if(withDetails)
    return entry + `: <i><span id="${id}">... inscrits, ... Km</span></i> </li></ul></div>`;
  return entry + "</div>"
}

/// Format numbers with french style and using ceil to round off
numberFormatter = new Intl.NumberFormat('fr-FR');
var formatter = function(value)
{
  return numberFormatter.format(Math.ceil(value))
}

totalKm = 0
function init(teamName, withDetails)
{
  $.ajax({
    url: URL+teamName+".json",
    dataType: "json",
    cache : false,
    success: function(json)
    {
      $( "meta[property='og:title']" ).attr("content", json.title);
      $( "meta[property='og:image']" ).attr("content", json.preview);
      $( "meta[name='twitter:title']" ).attr("content", json.title);
      $( "meta[name='twitter:image']" ).attr("content", json.preview);
      $('.title').text(json.title);
      $('#blason').attr("src", json.blason);
      if(json.blason===null)
        $('#blason').hide()
      $('#maincontainer').attr("style", json.background_style);
      load(json.teams, withDetails);
    }
  });
}

function load(teamsInGroup, withDetails)
{
  rows = "";
  columns = "";
  teams = Object.keys(teamsInGroup);
  teams = teams.sort(function(teamA,teamB){
    return teamsInGroup[teamA]["totalKmInsideBoundary"] <
           teamsInGroup[teamB]["totalKmInsideBoundary"]});
  for( index in teams )
  {
    team = teams[index];
    columns += getHtmlForTeamEntry(team, teamsInGroup[team], withDetails);
    if(index%2 === 1)
    {
      rows += "<div class='row'>"+columns+"</div>";
      columns="";
    }
  }
  if(columns)
    rows += "<div class='row'>"+columns+"</div>";
  document.querySelector('.teams').innerHTML = rows;

   // $.ajax({
   //    url: "https://www.naviki.org/naviki/api/v5/Contest/2/findContest/51090",
   //    dataType: "json",
   //    cache : false,
   //    success: function(json)
   //    {
   //      totalKm = json.totalKmInsideBoundary
   //     setNewValue( $("#totalKm"), 0, totalKm, formatter)
   //   }
   // });

  $.ajax({
    url: "./database/data.json",
    dataType: "json",
    cache : false,
    success: function(json)
    {
      teams = json.data
      for( team of teams )
      {
        if( team.name in teamsInGroup )
        {
          totalKmLille = team.progress
          numberOfMembersLille = team.total_members
          $("#"+teamsInGroup[team.name]).html( numberOfMembersLille + " inscrits, " + totalKmLille + " Km" )
        }
      }
      $("#spinner").addClass("d-none")
      $("#line1").removeClass("d-none")

      //setNewValue( $("#totalKm-lille"), 0, totalKmLille, formatter)
      //setNewValue( $("#numberOfMembers-lille"), 0, numberOfMembersLille, formatter)
      setNewValue( $("#numberOfTeams-lille"), 0, Object.keys(teamsInGroup).length, formatter)

      //setNewValue( $("#totalKm"), 0, totalKm, formatter)
      //setNewValue( $("#numberOfMembers"), 0, numberOfMembers, formatter)
      //setNewValue( $("#numberOfTeams"), 0, json.teams.length, formatter)
    } /// End of callback
  });
}
