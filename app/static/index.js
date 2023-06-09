var cal = {
  // (A) SET PROPERTIES
  // (A1) FLAGS & DATA
  mon : false,    // monday first
  events : null,  // events data for current month/year
  sMth : 0,       // selected month
  sYear : 0,      // selected year
  sDIM : 0,       // number of days in selected month
  sF : 0,         // first date of the selected month (yyyymmddhhmm)
  sL : 0,         // last date of the selected month (yyyymmddhhmm)
  sFD : 0,        // first day of the selected month (mon-sun)
  sLD : 0,        // last day of the selected month (mon-sun)
  ready : 0,      // to track loading

  // (A2) HTML & ELEMENTS
  hMth : null, hYear : null,      // month & year
  hCD : null, hCB : null,         // calendar days & body
  hFormWrap : null, hForm : null, // event form
  hfID : null, hfStart : null,    // event form fields
  hfEnd : null, hfTxt : null,
  hfColor : null, hfBG : null,
  hfDel : null,
  hfCategory : null,
  hfDetail : null,
  hfDet : null,
  //subevent//
  hfJS : null,


  // (B) SUPPORT FUNCTIONS
  ajax : (req, data, onload) => {
    // (B1) FORM DATA
    let form = new FormData();
    for (let [k,v] of Object.entries(data)) { form.append(k,v); }

    // (B2) AJAX FETCH
    fetch(req + "/", { method:"POST", body:form })
    .then(res => res.text())
    .then(txt => onload(txt))
    .catch(err => console.error(err));
  },

  // (C) INIT CALENDAR
  init : () => {
    // (C1) GET HTML ELEMENTS
    cal.hMth = document.getElementById("calMonth");
    cal.hYear = document.getElementById("calYear");
    cal.hCD = document.getElementById("calDays");
    cal.hCB = document.getElementById("calBody");
    cal.hFormWrap = document.getElementById("calForm");
    cal.hForm = cal.hFormWrap.querySelector("form");
    cal.hfID = document.getElementById("evtID");
    cal.hfStart = document.getElementById("evtStart");
    cal.hfEnd = document.getElementById("evtEnd");
    cal.hfTxt = document.getElementById("evtTxt");
    cal.hfColor = document.getElementById("evtColor");
    cal.hfBG = document.getElementById("evtBG");
    cal.hfDel = document.getElementById("evtDel");
    cal.hfCategory = document.getElementsByName("category");
    cal.hfDetail = document.getElementsByName("detail");
    cal.hfDet = document.getElementById("evtDet");
    //subevent//
    cal.hfJS = document.getElementById("js");

    // (C2) MONTH AND YEAR SELECTOR
    let now = new Date(), nowMth = now.getMonth() + 1;
    for (let [i,n] of Object.entries({
      1 : "JAN", 2 : "FEB", 3 : "MAR", 4 : "APR",
      5 : "MAY", 6 : "JUN", 7 : "JUL", 8 : "AUG",
      9 : "SEP", 10 : "OCT", 11 : "NOV", 12 : "DEC"
    })) {
      let opt = document.createElement("option");
      opt.value = i;
      opt.innerHTML = n;
      if (i==nowMth) { opt.selected = true; }
      cal.hMth.appendChild(opt);
    }
    cal.hYear.value = parseInt(now.getFullYear());

    // (C3) ATTACH CONTROLS
    cal.hMth.onchange = cal.load;
    cal.hYear.onchange = cal.load;
    document.getElementById("calBack").onclick = () => cal.pshift();
    document.getElementById("calNext").onclick = () => cal.pshift(1);
    document.getElementById("calAdd").onclick = () => cal.show();
    cal.hForm.onsubmit = () => cal.save();
    document.getElementById("evtCX").onclick = () => cal.hFormWrap.close();
    cal.hfDel.onclick = cal.del;
    cal.hfDet.onclick = () => window.location=`/events/${cal.hfID.value}`

    // (C4) DRAW DAY NAMES
    let days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"];
    if (cal.mon) { days.push("SUN"); } else { days.unshift("SUN"); }
    for (let d of days) {
      let cell = document.createElement("div");
      cell.className = "calCell";
      cell.innerHTML = d;
      cal.hCD.appendChild(cell);
    }

    // (C5) LOAD AND DRAW CALENDAR
    cal.load();
  },

  // (D) SHIFT CURRENT PERIOD BY SINGLE MONTH
  pshift : forward => {
    cal.sMth = parseInt(cal.hMth.value);
    cal.sYear = parseInt(cal.hYear.value);
    if (forward) { cal.sMth++; } else { cal.sMth--; }
    if (cal.sMth > 12) { cal.sMth = 1; cal.sYear++; }
    if (cal.sMth < 1) { cal.sMth = 12; cal.sYear--; }
    cal.hMth.value = cal.sMth;
    cal.hYear.value = cal.sYear;
    cal.load();
  },

  // (E) LOAD EVENTS
  load : () => {
    // (E1) SET EVENTS' SELECTED PERIOD
    cal.sMth = parseInt(cal.hMth.value);
    cal.sYear = parseInt(cal.hYear.value);
    cal.sDIM = new Date(cal.sYear, cal.sMth, 0).getDate();
    cal.sFD = new Date(cal.sYear, cal.sMth-1, 1).getDay();
    cal.sLD = new Date(cal.sYear, cal.sMth-1, cal.sDIM).getDay();
    let m = cal.sMth;
    if (m < 10) { m = "0" + m; }
    cal.sF = parseInt(String(cal.sYear) + String(m) + "010000");
    cal.sL = parseInt(String(cal.sYear) + String(m) + String(cal.sDIM) + "2359");

    // (E2) AJAX FETCH GET EVENTS
    cal.ajax("get", { month : cal.sMth, year : cal.sYear }, evt => {
      cal.events = JSON.parse(evt);
      cal.draw();
    });
  },

  // (F) DRAW CALENDAR
  draw : () => {
    // (F1) CALCULATE DAY MONTH & YEAR
    // note - jan is 0 & dec is 11 in js
    // note - sun is 0 & sat is 6 in js
    let now = new Date(),                       // current date
        nowMth = now.getMonth()+1,              // current month
        nowYear = parseInt(now.getFullYear()),  // current year
        nowDay = cal.sMth==nowMth && cal.sYear==nowYear ? now.getDate() : null ;

    // (F2) DRAW CALENDAR ROWS & CELLS
    // (F2-1) INIT AND HELPER FUNCTIONS
    let rowA, rowB, rowC, rowMap = {}, rowNum = 1,
        cell, cellNum = 1,
    rower = () => {
      rowA = document.createElement("div");
      rowB = document.createElement("div");
      rowC = document.createElement("div");
      rowA.className = "calRow";
      rowA.id = "calRow" + rowNum;
      rowB.className = "calRowHead";
      rowC.className = "calRowBack";
      cal.hCB.appendChild(rowA);
      rowA.appendChild(rowB);
      rowA.appendChild(rowC);
    },
    celler = day => {
      cell = document.createElement("div");
      cell.className = "calCell";
      if (day) { cell.innerHTML = day; }
      rowB.appendChild(cell);
      cell = document.createElement("div");
      cell.className = "calCell";
      if (day===undefined) { cell.classList.add("calBlank"); }
      if (day!==undefined && day==nowDay) { cell.classList.add("calToday"); }
      rowC.appendChild(cell);
    };
    cal.hCB.innerHTML = ""; rower();

    // (F2-2) BLANK CELLS BEFORE START OF MONTH
    if (cal.mon && cal.sFD != 1) {
      let blanks = cal.sFD==0 ? 7 : cal.sFD ;
      for (let i=1; i<blanks; i++) { celler(); cellNum++; }
    }
    if (!cal.mon && cal.sFD != 0) {
      for (let i=0; i<cal.sFD; i++) { celler(); cellNum++; }
    }

    // (F2-3) DAYS OF THE MONTH
    for (let i=1; i<=cal.sDIM; i++) {
      rowMap[i] = { r : rowNum, c : cellNum };
      celler(i);
      if (cellNum%7==0 && i!=cal.sDIM) { rowNum++; rower(); }
      cellNum++;
    }
    
    // (F2-4) BLANK CELLS AFTER END OF MONTH
    if (cal.mon && cal.sLD != 0) {
      let blanks = cal.sLD==6 ? 1 : 7-cal.sLD;
      for (let i=0; i<blanks; i++) { celler(); cellNum++; }
    }
    if (!cal.mon && cal.sLD != 6) {
      let blanks = cal.sLD==0 ? 6 : 6-cal.sLD;
      for (let i=0; i<blanks; i++) { celler(); cellNum++; }
    }

    // (F3) DRAW EVENTS
    if (Object.keys(cal.events).length > 0) { for (let [id,evt] of Object.entries(cal.events)) {
      // (F3-1) EVENT START END DAY
      let sd = new Date(evt.s), ed = new Date(evt.e);
      if (sd.getFullYear() < cal.sYear) { sd = 1; }
      else { sd = sd.getMonth()+1 < cal.sMth ? 1 : sd.getDate(); }
      if (ed.getFullYear() > cal.sYear) { ed = cal.sDIM; }
      else { ed = ed.getMonth()+1 > cal.sMth ? cal.sDIM : ed.getDate(); }

      // (F3-2) "MAP" ONTO HTML CALENDAR
      cell = {}; rowNum = 0;
      for (let i=sd; i<=ed; i++) {
        if (rowNum!=rowMap[i]["r"]) {
          cell[rowMap[i]["r"]] = { s:rowMap[i]["c"], e:0 };
          rowNum = rowMap[i]["r"];
        }
        if (cell[rowNum]) { cell[rowNum]["e"] = rowMap[i]["c"]; }
      }

      // (F3-3) 'DRAW' HTML EVENT ROW
      for (let [r,c] of Object.entries(cell)) {
        let o = c.s - 1 - ((r-1) * 7),              // event cell offset
            w = c.e - c.s + 1;                      // event cell width
        rowA = document.getElementById("calRow"+r);
        rowB = document.createElement("div");
        rowB.className = "calRowEvt";
        rowB.innerHTML = cal.events[id]["t"];
        rowB.style.color = cal.events[id]["c"];
        rowB.style.backgroundColor  = cal.events[id]["b"];
        rowB.classList.add("w"+w);
        if (o!=0) { rowB.classList.add("o"+o); }
        rowB.onclick = () => cal.show(id);
        rowA.appendChild(rowB);
      }
    }}
  },

  // (G) SHOW EVENTFORM
  show : id => {
    if (id) {
      cal.hForm.reset();
      cal.hfID.value = id;
      cal.hfStart.value = cal.events[id]["s"];
      cal.hfEnd.value = cal.events[id]["e"];
      cal.hfTxt.value = cal.events[id]["t"];
      cal.hfColor.value = cal.events[id]["c"];
      cal.hfBG.value = cal.events[id]["b"];
      cal.hfDel.style.display = "inline-block";
      cal.hfDet.style.display = "inline-block";
      cat = cal.events[id]["cat"];
      for(let idx=0; idx<cat.length; idx++) {
        val = cat[idx]
        cal.hfCategory[val-1].checked = true
      }
      det = cal.events[id]["det"];
      cal.hfDetail[0].value = det;
      //subevent//
      cal.hfJS.innerHTML = '';
      const sub = cal.events[id]["subs"];
      const html_js = document.getElementById("js");
      for (let idx=0; idx<sub.length; idx++) {
        id = sub[idx][0]
        ket = sub[idx][1]
        part = sub[idx][2]

        const html = `<div id="se_${id}" style="width: 100%; display: flex;">
        <div class="evt50">
          <label>Keterangan</label>
          <input value="${ket}" name="keterangan" type="text" required>
        </div>
        <div class="evt30">
          <label>Participant</label>
          <input value="${part}" name="participant" type="number" style="width: 100%; padding-top: 6px;" required>
        </div>
        <div class="evt20">
          <label>Remove</label>
          <button onclick="delSub(); return false;" style="width: 63%; background-color: rosybrown; border-color: rosybrown; padding-top: 3px;">-</button>
        </div>
        </div>`;

        html_js.insertAdjacentHTML('beforeend', html);
      }
    } else {
      cal.hForm.reset();
      cal.hfID.value = "";
      cal.hfDel.style.display = "none";
      cal.hfDet.style.display = "none";
      //subevent//
      cal.hfJS.innerHTML = '';
    }
    cal.hFormWrap.show();
  },

  // (H) SAVE EVENT
  save : () => {
    // (H1) COLLECT DATA
    // s & e  : start & end date
    // c & b  : text & background color
    // t      : event text
    var cat = [];
    var det = cal.hfDetail[0].value;
    
    for(let idx=0; idx<cal.hfCategory.length; idx++) {  
      if(cal.hfCategory[idx].checked)
        cat.push(cal.hfCategory[idx].value);
    }
    
    //subevent//
    var subs = {
      "update" : [],
      "create" : []
    }
    const html_js = document.getElementById("js");
    const html_js_children = html_js.children;
    for(let idx=0; idx<html_js_children.length; idx++) {  
      child = html_js_children[idx]
      id = child.id
      inputs = document.querySelectorAll(`#${id} input`);
      ket = inputs[0].value;
      part = inputs[1].value;
      if (id.startsWith('js')) {
        subs["create"].push([id.split('_')[1], ket, part]);
      } else if (id.startsWith('se')) {
        subs["update"].push([id.split('_')[1], ket, part]);
      }
    }

    var data = {
      s : cal.hfStart.value.replace("T", " "),
      e : cal.hfEnd.value.replace("T", " "),
      t : cal.hfTxt.value,
      c : cal.hfColor.value,
      b : cal.hfBG.value,
      det : det,
      cat : cat,
      //subevent//
      subs : JSON.stringify(subs)
    };
    if (cal.hfID.value != "") { data.id = parseInt(cal.hfID.value); }

    // (H2) DATE CHECK
    if (new Date(data.s) > new Date(data.e)) {
      alert("Start date cannot be later than end date!");
      return false;
    }

    // (H3) SAVE EVENT
    cal.ajax("save", data, res => {
      if (res=="OK") {
        cal.hFormWrap.close();
        cal.load();
      } else { alert(res); }
    });
    return false;
  },

  // (I) DELETE EVENT
  del : () => { if (confirm("Delete Event?")) {
    cal.ajax("cut", { "id" : parseInt(cal.hfID.value) }, res => {
      if (res=="OK") {
        cal.hFormWrap.close();
        cal.load();
      } else { alert(res); }
    });
  }}
};
window.onload = cal.init;