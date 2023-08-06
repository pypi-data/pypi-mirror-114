async function checkout(branch)
{
    if(confirm("确定切换至"+branch+"分支吗？"))
    {
        try
        {
            const response = await axios.post("/git/checkout?branch="+branch);
            console.log(response);
            if(response.status==200)
            {
                alert("切换成功。");
                location.reload();
            }
        }
        catch(err)
        {
            alert("切换失败。您可以查看服务控制台输出内容。");
        }
    }
}
async function new_remote_branch()
{
    var remote_branch_name=prompt("远程分支名：");
    if(!remote_branch_name)
    {
        return;
    }
    var remote_url=prompt("远程URL：");
    if(!remote_url)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/new_remote?name="+remote_branch_name+"&url="+remote_url);
        console.log(response)
        if(response.status==200)
        {
            alert("新建成功。");
            location.reload();
        }
    }
    catch(err)
    {
        alert("新建失败。您可以查看服务控制台输出内容。");
    }
}
async function remove_remote(name)
{
    if(!confirm("确定删除远程分支"+name+"吗？"))
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/remove_remote?name="+name);
        console.log(response)
        if(response.status==200)
        {
            alert("删除成功。");
            location.reload();
        }
    }
    catch(err)
    {
        alert("删除失败。您可以查看服务控制台输出内容。");
    }
}
async function new_branch()
{
    var name=prompt("远程分支名：");
    if(!name)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/new_branch?name="+name);
        console.log(response)
        if(response.status==200)
        {
            alert("新建成功。");
            location.reload();
        }
    }
    catch(err)
    {
        alert("新建失败。您可以查看服务控制台输出内容。");
    }
}
async function get_status()
{
    try
    {
        const response = await axios.post("/git/status");
        console.log(response)
        if(response.status==200)
        {
            var content=decodeURIComponent(response.data.result)
            document.getElementById("status").innerHTML=content;
        }
    }
    catch(err)
    {
        alert("获取文件编辑信息失败。您可以查看服务控制台输出内容。");
    }
}
get_status();
async function stage()
{
    try
    {
        const response = await axios.post("/git/stage");
        console.log(response)
        if(response.status==200)
        {
            get_status();
            alert("暂存成功。");
        }
    }
    catch(err)
    {
        alert("暂存失败。您可以查看服务控制台输出内容。");
    }
}
async function commit()
{
    info=prompt("请输入提交信息。不支持多行文本。");
    if(!info)
    {
        return;
    }
    try
    {
        const response = await axios.post("/git/commit?info="+encodeURIComponent(info));
        console.log(response)
        if(response.status==200)
        {
            alert("提交成功。");
            get_status();
        }
    }
    catch(err)
    {
        alert("提交失败。您可以查看服务控制台输出内容。");
    }
}
async function pull(remote,branch)
{
    if(!confirm(`确认拉取远程分支${remote}到本地分支${branch}吗？`))
    {
        return;
    }
    try
    {
        const response = await axios.post(`/git/pull?remote=${remote}&branch=${branch}`);
        console.log(response)
        if(response.status==200)
        {
            alert("拉取成功。");
            get_status();
        }
    }
    catch(err)
    {
        alert("拉取失败。您可以查看服务控制台输出内容。");
    }
}

async function push(remote,branch)
{
    if(!confirm(`确认推送本地分支${branch}到远程分支${remote}吗？`))
    {
        return;
    }
    try
    {
        const response = await axios.post(`/git/push?remote=${remote}&branch=${branch}`);
        console.log(response)
        if(response.status==200)
        {
            alert("推送成功。");
            get_status();
        }
    }
    catch(err)
    {
        alert("推送失败。您可以查看服务控制台输出内容。");
    }
}