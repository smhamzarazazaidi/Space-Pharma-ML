function formattedDate(rawDate){
  date = new Date(rawDate).toLocaleString('en-US', {
    month: 'short',
    day: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });

  return date
}

function milestones(dataJSON) {
  if (dataJSON) {
    var data_plots = JSON.parse(dataJSON.telemetry_data);
    if (Object.keys(data_plots).length == 0) {
      var data_plots = JSON.parse(dataJSON.radiation_data);
    }
    var milestones = data_plots.milestones;

    //console.log(milestones)
    html = document.getElementById('milestones-card-body').innerHTML.trim();
    html += '<div style="background:white;padding: 10px">';
    for (let key in milestones) {
      //console.log(key)
      if (key.replaceAll('_', ' ') == 'Launch' || key.replaceAll('_', ' ') == 'launch') {
        tooltip =
          "<a data-toggle='tooltip' data-placement='right' data-html='true' onclick='tooltipFcn(this)' title='On this date the mission launched.'><i class='material-icons-outlined' style='font-size: 12px;color:#555555' >info</i></a>";
      } else if (key.replaceAll('_', ' ') == 'Reached orbit') {
        tooltip =
          "<a data-toggle='tooltip' data-placement='right' data-html='true' onclick='tooltipFcn(this)' title='On this date the vehicle reached orbit.'><i class='material-icons-outlined' style='font-size: 12px; color:#555555' >info</i></a>";
      } else if (key.replaceAll('_', ' ') == 'Animal transfer to ISS') {
        tooltip =
          "<a data-toggle='tooltip' data-placement='right' data-html='true' onclick='tooltipFcn(this)' title='On this date rodents were transferred into a habitat module.'><i class='material-icons-outlined' style='font-size: 12px;color:#555555' >info</i></a>";
      } else if (
        key.replaceAll('_', ' ') == 'Sacrifice 1' ||
        key.replaceAll('_', ' ') == 'Sacrifice 2' ||
        key.replaceAll('_', ' ') == 'Sacrifice 3' ||
        key.replaceAll('_', ' ') == 'Sacrifice 4' ||
        key.replaceAll('_', ' ') == 'sac2' ||
        key.replaceAll('_', ' ') == 'sac3' ||
        key.replaceAll('_', ' ') == 'sac4' ||
        key.replaceAll('_', ' ') == 'Sac4'
      ) {
        tooltip =
          "<a data-toggle='tooltip' data-placement='right' data-html='true' onclick='tooltipFcn(this)' title='On this date a cohort of rodents was euthanized.'><i class='material-icons-outlined' style='font-size: 12px;color:#555555' >info</i></a>";
      } else if (key.replaceAll('_', ' ') == 'Sample Return') {
        tooltip =
          "<a data-toggle='tooltip' data-placement='right' data-html='true' onclick='tooltipFcn(this)' title='On this date the vehicle landed back on Earth.'><i class='material-icons-outlined' style='font-size: 12px;color:#555555' >info</i></a>";
      } else if (key.replaceAll('_', ' ') == 'animal transfer to ISS') {
        tooltip =
          "<a data-toggle='tooltip' data-placement='right' data-html='true' onclick='tooltipFcn(this)' title='On this date rodents were transferred into a habitat module.'><i class='material-icons-outlined' style='font-size: 12px;color:#555555' >info</i></a>";
      } else {
        tooltip = '';
      }
      html +=
        '<p class="card-subtitle mb-2"><input style="margin-right:4px" class="milestone-checkbox" type="checkbox" id="'+ key.replaceAll(" ", "_") +'">' +
        key.replaceAll('_', ' ') +
        ' ' +
        tooltip +
        ': <span class="card-subtitle mb-2 text-muted" style="font-size:1em">' +
        formattedDate(milestones[key]) +
        '</span></p>';
    }
    html += '</div>';

    if (Object.keys(milestones).length == 0) {
      var mission = document.getElementById('dropdownMenuButton1').innerHTML;
      html = html.split('</div>')[0];
      html += '<p>The mission milestones for ' + mission + ' are coming soon!<p/></div>';
    }
    document.getElementById('milestones-card-body').innerHTML = html;

    const elements = document.querySelectorAll('.milestone-checkbox');
      elements.forEach((element) => {
        element.addEventListener('change', function(){
          telemetry_plot(data, 'temperature')
          telemetry_plot(data, 'rh')
          radiation_plot(data, 'gcr')
          radiation_plot(data, 'saa')
          radiation_plot(data, 'accumulated')
          all_radiation_plot(data)
          if(document.getElementById("dropdownMenuButton1").innerHTML.includes("RR-")){
            telemetry_plot(data, 'co2')
          }else{
            document.getElementById("co2").innerHTML = "There is no CO2 data available for " + document.getElementById("dropdownMenuButton1").innerHTML + " ."
          }
        });
    });
  }
}

function telemetry_plot(dataJSON, type) {
  if (dataJSON) {
    var data_plots = JSON.parse(dataJSON.telemetry_data);

    if (Object.keys(data_plots).length == 0) {
      document.getElementById('temperature').innerHTML = 'There is no available Telemetry data for the selected mission.';
      document.getElementById('rh').innerHTML = '';
      document.getElementById('co2').innerHTML = '';
    } else {
      console.log(type);
      var data_ground = data_plots[type + '_ground'];
      var data_iss = data_plots[type + '_iss'];
      console.log(data_plots);
      console.log('data_ground');
      console.log(data_ground);
      console.log('data_iss');
      console.log(data_iss);

      //console.log(data_ground)

      if (document.getElementById('telemetryRelativeDateSwitch').checked) {
        var xaxis_text = 'Days after launch';

        var mission = document.getElementById('dropdownMenuButton1').innerHTML;
        var firstValidIndex_ground = data_ground.findIndex((item) => item !== 'NA');
        var data_ground = data_ground.slice(firstValidIndex_ground);
        //console.log(data_ground)

        var firstValidIndex_iss = data_iss.findIndex((item) => item !== 'NA');
        var data_iss = data_iss.slice(firstValidIndex_iss);
        //console.log(data_iss)

        if (mission.includes('RR')) {
          var time_ground = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 5) / 1440);
          var time_iss = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 5) / 1440);
        } else if (mission.includes('APEX')) {
          var time_ground = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 10) / 1440);
          var time_iss = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 10) / 1440);
        } else if (mission == 'VEG-01A') {
          var time_ground = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 15) / 1440);
          var time_iss = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 15) / 1440);
        } else if (mission == 'VEG-01C') {
          var time_ground = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 5) / 1440);
          var time_iss = Array.from({ length: Math.max(data_ground.length, data_iss.length) }, (value, index) => (index * 5) / 1440);
        }
      } else {
        var time_ground = data_plots.time;
        var time_iss = data_plots.time;
        var xaxis_text = 'Date [MMM D, YYYY HH:mm]';
      }

      //console.log(time)
      //console.log(data_ground)

      
      var trace_ground = {
        type: 'scatter',
        mode: 'lines',
        name: 'Ground',
        x: time_ground,
        y: data_ground
      };

      var trace_iss = {
        type: 'scatter',
        mode: 'lines',
        name: 'ISS',
        x: time_iss,
        y: data_iss
      };

      var data = [trace_ground, trace_iss];
      //console.log("type")
      //console.log(type)
      if (type == 'temperature') {
        yaxis = 'Degrees [C]';
        title = 'Temperature';
      } else if (type == 'rh') {
        yaxis = 'RH [%]';
        title = 'Relative Humidity (RH)';
      } else if (type == 'co2') {
        yaxis = 'CO2 [ppm]';
        title = 'CO2';
      }

      shapes = [];
      annotations = [];
      //if (document.getElementById('showMilestones').checked == true) {
        if (document.getElementById('telemetryRelativeDateSwitch').checked) {
          var exact_milestones = data_plots.milestones;
          var milestones = {};
          for (let key in exact_milestones) {
            milestones[key] = (data_plots.time.indexOf(exact_milestones[key] + ':00') * 5) / 1440;
          }
        } else {
          var milestones = data_plots.milestones;
        }

        var i = 0;
        for (let key in milestones) {
          if(document.getElementById(key.replaceAll(" ", "_")).checked){
            shapes.push({
              type: 'line',
              x0: milestones[key],
              y0: 0,
              x1: milestones[key],
              yref: 'paper',
              y1: 1,
              line: {
                color: 'grey',
                width: 1.5,
                dash: 'dot'
              }
            });
            annotations.push({
              x: milestones[key],
              y: 1,
              xref: 'x',
              yref: 'paper',
              text: key,
              showarrow: true,
              ax: 10,
              ay: -10 - i,
              arrowhead: 4
            });
            i += 8;
          }
        }
      //}

      if(document.getElementById("dropdownMenuButton1").innerText == "RR-10" || document.getElementById("dropdownMenuButton1").innerText == "RR-20"){
          time_ground.length = time_ground.length -1
          data_ground.length = data_ground.length -1
          time_iss.length = time_iss.length -1
          data_iss.length = data_iss.length -1
      }

      if(document.getElementById("dropdownMenuButton1").innerText == "RR-18"){
        //time_ground.length = time_ground.length -1
        //data_ground.length = data_ground.length -1
        time_iss.length = time_iss.length -1
        data_iss.length = data_iss.length -1
    }
      var layout = {
        title: title,
        yaxis: {
          title: {
            text: yaxis
          }
        },
        xaxis: {
          title: {
            text: xaxis_text
          }
        },
        shapes: shapes,
        annotations: annotations
      };

      Plotly.newPlot(type, data, layout);
    }
  }
}
