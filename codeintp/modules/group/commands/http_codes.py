from arclet.alconna import Alconna, Arg, Arparma
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="查看机器人帮助",
    usage=""
)

http_codes = on_alconna(
    Alconna("http", Arg("code", int)),
    use_cmd_start=True,
    priority=10
)

codes = [
    "100",
    "101",
    "200",
    "201",
    "202",
    "203",
    "204",
    "205",
    "206",
    "301",
    "302",
    "303",
    "304",
    "305",
    "400",
    "401",
    "403",
    "404",
    "405",
    "406",
    "407",
    "408",
    "409",
    "411",
    "412",
    "413",
    "414",
    "415",
    "416",
    "417",
    "418",
    "451",
    "500",
    "501",
    "502",
    "503",
    "504"
]

explanations = [
    "100 Continue\n服务器已经接收到请求头，并且客户端应继续发送请求主体（在需要发送身体的请求的情况下：例如，POST请求），或者如果请求已经完成，忽略这个响应。",
    "101 Switching Protocols\n服务器已经理解了客户端的请求，并将通过Upgrade消息头通知客户端采用不同的协议来完成这个请求。"
    "在发送完这个响应最后的空行后，服务器将会切换到在Upgrade消息头中定义的那些协议。",
    "200 OK\r\nok啊，请求成功辣（喜）",
    "201 Created\n请求已经被实现，而且有一个新的资源已经依据请求的需要而创建，且其URI已经随Location头信息返回。假如需要的资源无法及时创建的话，应当返回'202 Accepted'。",
    "202 Accepted\n服务器已接受请求，但尚未处理。最终该请求可能会也可能不会被执行，并且可能在处理发生时被禁止。",
    "203 Non-Authoritative Information\n服务器是一个转换代理服务器，以200 OK状态码为起源，但回应了原始响应的修改版本。",
    "204 No Content\n服务器成功处理了请求，没有返回任何内容。"
    "在强制门户功能中，Wi-Fi 设备连接到需要进行 Web 认证的 Wi-Fi 接入点时，通过访问一个能生成 HTTP 204 响应的的网站，"
    "如果能正常收到 204 响应，则代表无需 Web 认证，否则会弹出网页浏览器界面，显示出 Web 网页认证界面用于让用户认证登录。",
    "205 Reset Content\n服务器成功处理了请求，但没有返回任何内容。与204响应不同，此响应要求请求者重置文档视图。",
    "206 Partial Content\n服务器已经成功处理了部分GET请求。类似于FlashGet或者迅雷这类的HTTP下载工具都是使用此类响应实现断点续传或者将一个大文档分解为多个下载段同时下载。",
    "301 Moved Permanently\n宁害用这个链接？让我带你前往新的链接罢！",
    "302 Found\n要求客户端执行临时重定向（原始描述短语为“Moved Temporarily”）。由于这样的重定向是临时的，客户端应当继续向原有地址发送以后的请求。",
    "303 See Other\n对应当前请求的响应可以在另一个URI上被找到，当响应于POST（或PUT / DELETE）接收到响应时，客户端应该假定服务器已经收到数据，并且应该使用单独的GET消息发出重定向。",
    "304 Not Modified\n表示资源在由请求头中的If-Modified-Since或If-None-Match参数指定的这一版本之后，未曾被修改。",
    "305 Use Proxy\n被请求的资源必须通过指定的代理才能被访问。Location域中将给出指定的代理所在的URI信息，接收者需要重复发送一个单独的请求，通过这个代理才能访问相应资源。",
    "400 Bad Request\n服务器：这是你的问题，不是我的问题（恼）",
    "401 Unauthorized\n用户名密码都不知道，宁还想进来？（恼）",
    "403 Forbidden\n这事宁该来的地方吗？（恼）",
    "404 Not Found\n这个错误码最好献给你的对象（雾）",
    "405 Method Not Allowed\n请求行中指定的请求方法不能被用于请求相应的资源。该响应必须返回一个Allow头信息用以表示出当前资源能够接受的请求方法的列表。",
    "406 Not Acceptable\n请求的资源的内容特性无法满足请求头中的条件，因而无法生成响应实体，该请求不可接受。",
    "407 Proxy Authentication Required\n与401响应类似，只不过客户端必须在代理服务器上进行身份验证。",
    "408 Request Timeout\n请求超时。根据HTTP规范，客户端没有在服务器预备等待的时间内完成一个请求的发送，客户端可以随时再次提交这一请求而无需进行任何更改。",
    "409 Conflict\n表示因为请求存在冲突无法处理该请求，例如多个同步更新之间的编辑冲突。",
    "411 Length Required\n服务器拒绝在没有定义Content-Length头的情况下接受请求。在添加了表明请求消息体长度的有效Content-Length头之后，客户端可以再次提交该请求。",
    "412 Precondition Failed\n服务器在验证在请求的头字段中给出先决条件时，没能满足其中的一个或多个。",
    "413 Request Entity Too Large\n服务器拒绝处理当前请求，因为该请求提交的实体数据大小超过了服务器愿意或者能够处理的范围。",
    "414 Request-URI Too Long\n请求的URI长度超过了服务器能够解释的长度，因此服务器拒绝对该请求提供服务。通常将太多数据的结果编码为GET请求的查询字符串，在这种情况下，应将其转换为POST请求。",
    "415 Unsupported Media Type\n对于当前请求的方法和所请求的资源，请求中提交的互联网媒体类型并不是服务器中所支持的格式，因此请求被拒绝。"
    "例如，客户端将图像上传格式为svg，但服务器要求图像使用上传格式为jpg。",
    "416 Requested Range Not Satisfiable\n客户端已经要求文件的一部分，但服务器不能提供该部分。例如，如果客户端要求文件的一部分超出文件尾端。",
    "417 Expectation Failed\n在请求头Expect中指定的预期内容无法被服务器满足，或者这个服务器是一个代理服显的证据证明在当前路由的下一个节点上，Expect的内容无法被满足。",
    "418 I'm a teapot\n我摊牌了，我就是个茶壶（雾）",
    "451 Unavailable For Legal Reasons\n*内容被删除*",
    "500 Internal Server Error\n一看又是你服务器出问题辣（确信）",
    "501 Not Implemented\n服务器不支持当前请求所需要的某个功能。当服务器无法识别请求的方法，并且无法支持其对任何资源的请求。",
    "502 Bad Gateway\n作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应。（经典永流传属于是）",
    "503 Service Unavailable\n由于临时的服务器维护或者过载，服务器当前无法处理请求。这个状况是暂时的，并且将在一段时间以后恢复。（服务器：和蔼！任何DDoS，终将绳之以法！）",
    "504 Gateway Timeout\n作为网关或者代理工作的服务器尝试执行请求时，未能及时从上游服务器（URI标识出的服务器，例如HTTP、FTP、LDAP）或者辅助服务器（例如DNS）收到响应。"
]


@http_codes.handle()
async def handle_function(event: GroupMessageEvent, result: Arparma):
    code = str(result.query("code"))
    if code in codes:
        await http_codes.send(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 正在加载，请稍候……")
        ]))
        message_chain = Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text("\n"),
            MessageSegment.text(explanations[codes.index(code)]),
            MessageSegment.image(f"https://http.cat/{code}")
        ])
        await http_codes.finish(message_chain)
    else:
        await http_codes.finish(Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.at(event.sender.user_id),
            MessageSegment.text(" 未找到关于该状态码的解释")
        ]))
