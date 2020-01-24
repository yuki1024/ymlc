import { json } from "/result_snedo01_snc4_ilmax_arranged.csv_json.js";
//console.log(json);

function createMainBody(){
	let s = '';

	s+= '<div class="grid" id="grid0" style="top: 0px; left: 0px;"></div>';
	s+= '<div class="grid" id="grid1" style="top: 0px; left: 400px;"></div>';
	s+= '<div class="grid" id="grid2" style="top: 0px; left: 800px;"></div>';
	s+= '<div class="grid" id="grid3" style="top: 0px; left: 1200px;"></div>';
	s+= '<div class="grid" id="grid4" style="top: 300px; left: 0px;"></div>';
	s+= '<div class="grid" id="grid5" style="top: 300px; left: 400px;"></div>';
	s+= '<div class="grid" id="grid6" style="top: 300px; left: 800px;"></div>';
	s+= '<div class="grid" id="grid7" style="top: 300px; left: 1200px;"></div>';
	s+= '<div class="grid" id="grid8" style="top: 600px; left: 0px;"></div>';
	s+= '<div class="grid" id="grid9" style="top: 600px; left: 400px;"></div>';
	s+= '<div class="grid" id="grid10" style="top: 600px; left: 800px;"></div>';
	s+= '<div class="grid" id="grid11" style="top: 600px; left: 1200px;"></div>';

	document.querySelector('#all_body').insertAdjacentHTML('beforeend', s);

	for(let i=0; i<Object.keys(json).length; i++){
		s = '';
		console.log();
		for(let j=0; j<76; j++){
			s+= '<div class="cr core'+j+' dd" style="'+(j%2===0 ? 'display: none' : '')+'"></div>';
		}
		document.querySelector('#grid'+i).insertAdjacentHTML('beforeend', s);
	}

	let count = 0;
	Object.keys(json).forEach(function(k){
    var grid = document.getElementById("grid"+count);

   	let vals = Object.values(json[k]);
   	let cmax = Math.max(...vals);
   	let cmin = Math.min(...vals);

    for(let i=0; i<grid.children.length; i++){
    	if(String(i) in json[k]){
    		let num = json[k][String(i)];
    		let num_s = Math.round(num*10)/10;
		    grid.children[i].style.backgroundColor = coloring(num,cmin,cmax);
	    	grid.children[i].insertAdjacentHTML('beforeend', '<div class="crtext">'+i+'\n'+num_s+'</div>');
    	} else {
    		//no result, disabled cores
	    	grid.children[i].insertAdjacentHTML('beforeend', '<div class="crtext">'+i+'\n</div>');
    	}

    }

    //mem,interleaveのタイトルを挿入
   	grid.insertAdjacentHTML('beforeend', '<div class="gridtitle">'+k+'</div>');

		count++;
	});

}


function coloring(num,cmin,cmax){
	//pink rgb(255,0,255)
	//cyan rgb(0,255,255)

	let range = cmax-cmin;
	let red = Math.floor(255.0*(num-cmin)/range);
	let green = Math.floor(255.0*(cmax-num)/range);

	let color_s = 'rgb(' + String(red) + ',' + String(green) + ',255)';

	//return 'rgb(255,0,0)';
	return color_s;
}

//----------------------main---------------------
createMainBody();


//-------------------------------------------
//copied & pasted & modified??
(function(){

    //要素の取得
    var elements = document.getElementsByClassName("dd");

    //要素内のクリックされた位置を取得するグローバル（のような）変数
    var x;
    var y;

    //マウスが要素内で押されたとき、又はタッチされたとき発火
    for(var i = 0; i < elements.length; i++) {
        elements[i].addEventListener("mousedown", mdown, false);
        elements[i].addEventListener("touchstart", mdown, false);
    }

    //マウスが押された際の関数
    function mdown(e) {

        //クラス名に .drag を追加
        this.classList.add("drag");

        //タッチデイベントとマウスのイベントの差異を吸収
        if(e.type === "mousedown") {
            var event = e;
        } else {
            var event = e.changedTouches[0];
        }

        //要素内の相対座標を取得
        x = event.pageX - this.offsetLeft;
        y = event.pageY - this.offsetTop;

        //ムーブイベントにコールバック
        document.body.addEventListener("mousemove", mmove, false);
        document.body.addEventListener("touchmove", mmove, false);
    }

    //マウスカーソルが動いたときに発火
    function mmove(e) {

        //ドラッグしている要素を取得
        var drag = document.getElementsByClassName("drag")[0];

        //同様にマウスとタッチの差異を吸収
        if(e.type === "mousemove") {
            var event = e;
        } else {
            var event = e.changedTouches[0];
        }

        //フリックしたときに画面を動かさないようにデフォルト動作を抑制
        e.preventDefault();

        //マウスが動いた場所に要素を動かす
        drag.style.top = event.pageY - y + "px";
        drag.style.left = event.pageX - x + "px";

        //-------------------------------------------------------------
        let same_core_list = document.getElementsByClassName((drag.className.split(' '))[1]);

        for(i=0; i<same_core_list.length; i++){
        	same_core_list[i].style.top = event.pageY - y + "px";
        	same_core_list[i].style.left = event.pageX - x + "px";
        }


        //-------------------------------------------------------------

        //マウスボタンが離されたとき、またはカーソルが外れたとき発火
        drag.addEventListener("mouseup", mup, false);
        document.body.addEventListener("mouseleave", mup, false);
        drag.addEventListener("touchend", mup, false);
        document.body.addEventListener("touchleave", mup, false);

    }

    //マウスボタンが上がったら発火
    function mup(e) {
        var drag = document.getElementsByClassName("drag")[0];

        //ムーブイベントハンドラの消去
        document.body.removeEventListener("mousemove", mmove, false);
        drag.removeEventListener("mouseup", mup, false);
        document.body.removeEventListener("touchmove", mmove, false);
        drag.removeEventListener("touchend", mup, false);

        //クラス名 .drag も消す
        drag.classList.remove("drag");
    }

})()



