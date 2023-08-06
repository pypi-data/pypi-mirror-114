function save()
{
	var bottom_div=document.getElementById("main-control2").contentWindow.document.getElementById("bottom_div");
	var left_span=document.getElementById("main-control2").contentWindow.document.getElementById("left-span");
	bottom_div.style.background="#0033FF";
	left_span.innerHTML="保存中，请稍等";
	editor=ace.edit("editor");
	var save_value=editor.getValue();
	console.log(save_value);
	var send_value=encodeURIComponent(save_value);
	//console.log(GetQueryString("path"));
	try
	{
	    axios.post("/save?path="+encodeURIComponent(GetQueryString("path")),data=send_value).
		then(function(response)
			{
				console.log(response);
				if(response.status==200)
				{
					bottom_div.style.background="#38b400";
					left_span.innerHTML="已保存，就绪";
				}
				else
				{
					bottom_div.style.background="red";
					left_span.innerHTML="保存失败，请查看服务控制台或Console";
				}
			}
		);
	}
	catch(err)
	{
	    bottom_div.style.background="red";
		left_span.innerHTML="保存失败，请查看服务控制台或Console";
	}
}