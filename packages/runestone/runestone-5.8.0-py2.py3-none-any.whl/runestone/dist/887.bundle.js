(self.webpackChunkWebComponents=self.webpackChunkWebComponents||[]).push([[887],{2568:(e,t,i)=>{"use strict";i.d(t,{Z:()=>o});var s=i(21294);class o{constructor(e){this.component_ready_promise=new Promise((e=>this._component_ready_resolve_fn=e)),this.optional=!1,e&&(this.sid=e.sid,this.graderactive=e.graderactive,this.showfeedback=!0,e.timed&&(this.isTimed=!0),e.enforceDeadline&&(this.deadline=e.deadline),$(e.orig).data("optional")?this.optional=!0:this.optional=!1,e.selector_id&&(this.selector_id=e.selector_id),void 0!==e.assessmentTaken?this.assessmentTaken=e.assessmentTaken:this.assessmentTaken=!0,void 0!==e.timedWrapper?this.timedWrapper=e.timedWrapper:location.href.indexOf("doAssignment")>=0?this.timedWrapper=$("h1#assignment_name").text():this.timedWrapper=null,$(e.orig).data("question_label")&&(this.question_label=$(e.orig).data("question_label"))),this.jsonHeaders=new Headers({"Content-type":"application/json; charset=utf-8",Accept:"application/json"})}async logBookEvent(e){if(this.graderactive)return;let t;if(e.course=eBookConfig.course,e.clientLoginStatus=eBookConfig.isLoggedIn,e.timezoneoffset=(new Date).getTimezoneOffset()/60,this.percent&&(e.percent=this.percent),eBookConfig.useRunestoneServices&&eBookConfig.logLevel>0){let i=new Request(eBookConfig.ajaxURL+"hsblog",{method:"POST",headers:this.jsonHeaders,body:JSON.stringify(e)});try{let e=await fetch(i);if(!e.ok)throw new Error("Failed to save the log entry");t=e.json()}catch(e){this.isTimed&&alert(`Error: Your action was not saved! The error was ${e}`),console.log(`Error: ${e}`)}}return this.isTimed&&!eBookConfig.debug||console.log("logging event "+JSON.stringify(e)),"function"==typeof s.j.updateProgress&&"edit"!=e.act&&0==this.optional&&s.j.updateProgress(e.div_id),t}async logRunEvent(e){let t="done";if(!this.graderactive){if(e.course=eBookConfig.course,e.clientLoginStatus=eBookConfig.isLoggedIn,e.timezoneoffset=(new Date).getTimezoneOffset()/60,(this.forceSave||"to_save"in e==0)&&(e.save_code="True"),eBookConfig.useRunestoneServices&&eBookConfig.logLevel>0){let i=new Request(eBookConfig.ajaxURL+"runlog.json",{method:"POST",headers:this.jsonHeaders,body:JSON.stringify(e)}),s=await fetch(i);if(!s.ok)throw new Error("Failed to log the run");t=await s.json()}return this.isTimed&&!eBookConfig.debug||console.log("running "+JSON.stringify(e)),"function"==typeof s.j.updateProgress&&0==this.optional&&s.j.updateProgress(e.div_id),t}}async checkServer(e,t=!1){let i=this;if(this.checkServerComplete=new Promise((function(e,t){i.csresolver=e})),this.useRunestoneServices||this.graderactive){let t={};if(t.div_id=this.divid,t.course=eBookConfig.course,t.event=e,this.graderactive&&this.deadline&&(t.deadline=this.deadline,t.rawdeadline=this.rawdeadline,t.tzoff=this.tzoff),this.sid&&(t.sid=this.sid),!eBookConfig.practice_mode&&this.assessmentTaken){let e=new Request(eBookConfig.ajaxURL+"getAssessResults",{method:"POST",body:JSON.stringify(t),headers:this.jsonHeaders});try{let i=await fetch(e);t=await i.json(),this.repopulateFromStorage(t),this.csresolver("server")}catch(e){try{this.checkLocalStorage()}catch(e){console.log(e)}}}else this.loadData({}),this.csresolver("not taken")}else this.checkLocalStorage(),this.csresolver("local");t&&this.indicate_component_ready()}indicate_component_ready(){this.containerDiv.classList.add("runestone-component-ready"),this._component_ready_resolve_fn()}loadData(e){return null}repopulateFromStorage(e){null!==e&&this.shouldUseServer(e)?(this.restoreAnswers(e),this.setLocalStorage(e)):this.checkLocalStorage()}shouldUseServer(e){if("T"===e.correct||0===localStorage.length||!0===this.graderactive||this.isTimed)return!0;let t,i=localStorage.getItem(this.localStorageKey());if(null===i)return!0;try{t=JSON.parse(i)}catch(e){return console.log(e.message),localStorage.removeItem(this.localStorageKey()),!0}if(e.answer==t.answer)return!0;let s=new Date(t.timestamp);return new Date(e.timestamp)>=s}localStorageKey(){return eBookConfig.email+":"+eBookConfig.course+":"+this.divid+"-given"}addCaption(e){if(!this.isTimed){var t=document.createElement("p");this.question_label?(this.caption=`Activity: ${this.question_label} ${this.caption}  <span class="runestone_caption_divid">(${this.divid})</span>`,$(t).html(this.caption),$(t).addClass(`${e}_caption`)):($(t).html(this.caption+" ("+this.divid+")"),$(t).addClass(`${e}_caption`),$(t).addClass(`${e}_caption_text`)),this.capDiv=t,this.containerDiv.appendChild(t)}}hasUserActivity(){return this.isAnswered}checkCurrentAnswer(){console.log("Each component should provide an implementation of checkCurrentAnswer")}async logCurrentAnswer(){console.log("Each component should provide an implementation of logCurrentAnswer")}renderFeedback(){console.log("Each component should provide an implementation of renderFeedback")}disableInteraction(){console.log("Each component should provide an implementation of disableInteraction")}}window.RunestoneBase=o},97887:(e,t,i)=>{"use strict";i.r(t);var s=i(2568),o={};class a extends s.Z{constructor(e){super(e);var t=e.orig;this.origElem=t,this.divid=t.id,this.inactive=!1,$(this.origElem).is("[data-inactive]")&&(this.inactive=!0),this.togglesList=[],this.childTabs=[],this.populateChildTabs(),this.activeTab=0,this.findActiveTab(),this.createTabContainer(),this.indicate_component_ready()}populateChildTabs(){for(var e=0;e<this.origElem.childNodes.length;e++)"tab"===$(this.origElem.childNodes[e]).data("component")&&this.childTabs.push(this.origElem.childNodes[e])}findActiveTab(){for(var e=0;e<this.childTabs.length;e++)$(this.childTabs[e]).is("[data-active]")&&(this.activeTab=e)}createTabContainer(){this.containerDiv=document.createElement("div"),this.containerDiv.id=this.divid,$(this.containerDiv).addClass(this.origElem.getAttribute("class")),$(this.containerDiv).attr({role:"tabpanel"}),this.tabsUL=document.createElement("ul"),this.tabsUL.id=this.divid+"_tab",$(this.tabsUL).addClass("nav nav-tabs"),$(this.tabsUL).attr({role:"tablist"}),this.tabContentDiv=document.createElement("div"),$(this.tabContentDiv).addClass("tab-content"),this.createTabs(),this.containerDiv.appendChild(this.tabsUL),this.containerDiv.appendChild(this.tabContentDiv),this.addCMD(),$(this.origElem).replaceWith(this.containerDiv)}createTabs(){for(var e=0;e<this.childTabs.length;e++){var t=document.createElement("li");$(t).attr({role:"presentation","aria-controls":this.divid+"-"+e});var i=document.createElement("a");$(i).attr({"data-toggle":"tab",href:"#"+this.divid+"-"+e,role:"tab"});var s=document.createElement("span");s.textContent=$(this.childTabs[e]).data("tabname"),i.appendChild(s),t.appendChild(i),this.tabsUL.appendChild(t);var o=document.createElement("div");o.id=this.divid+"-"+e,$(o).addClass("tab-pane"),$(o).attr({role:"tabpanel"}),o.appendChild(this.childTabs[e]),this.inactive||this.activeTab===e&&($(t).addClass("active"),$(o).addClass("active")),this.togglesList.push(i),this.tabContentDiv.appendChild(o)}}addCMD(){$(this.togglesList).on("shown.bs.tab",(function(e){var t=$(e.target.attributes.href.value);t.find(".disqus_thread_link").each((function(){$(this).click()})),t.find(".CodeMirror").each((function(e,t){t.CodeMirror.refresh()}))}))}}$(document).ready((function(){$("[data-component=tabbedStuff]").each((function(e){o[this.id]=new a({orig:this})}))}))}}]);
//# sourceMappingURL=887.bundle.js.map?v=1e00b4e13aaaf1c1f880