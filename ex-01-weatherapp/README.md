
# 使用 GPT 进行多任务函数调用

## 问题描述

用户希望了解如何利用 GPT 的函数调用功能来执行多个任务，具体来说，用户想要查询两个城市的天气，并将查询结果保存到一个文本文件中。

## 解决方案

### 1. 定义外部函数

定义用于获取天气信息和保存数据到文件的两个函数。

```python
def get_current_weather(location, unit="fahrenheit"):
    # 实现获取天气信息的代码
    return {"location": location, "weather": "Sunny"}

def save_to_file(content, filename):
    # 实现将内容保存到文件的代码
    return {"status": "success", "message": f"Content saved to {filename}"}
```

### 2. 描述函数

在 API 调用中描述这些函数，包括函数名称、描述、参数等。

```python
functions = [
    {"name": "get_current_weather", "description": "Get the current weather in a given location", "parameters": {...}},
    {"name": "save_to_file", "description": "Save content to a TXT file", "parameters": {...}}
]
```

### 3. 利用 GPT 进行函数调用

通过设置 `function_call="auto"`，允许 GPT 根据聊天上下文自动决定是否调用外部函数。

```python
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=functions,
    function_call="auto",
)
```

### 4. 处理函数调用请求

解析 GPT 的响应，调用请求的函数，并获取函数的响应。

```python
if response_message.get("function_call"):
    function_name = response_message["function_call"]["name"]
    function_args = json.loads(response_message["function_call"]["arguments"])
    function_response = call_function(function_name, function_args)
```

### 5. 集成函数响应到聊天中

将函数的响应作为新消息追加到聊天中，并继续与 GPT 对话。

```python
messages.append({"role": "function", "name": function_name, "content": json.dumps(function_response)})
```

## 处理对话结束条件：`finish_reason`

### 关键技巧

在使用 GPT 进行函数调用的过程中，我们需要监控对话是否已达到其自然结束点。这可以通过检查 GPT 响应中的 `finish_reason` 来实现。

### 解决方案

#### 1. 监控对话结束条件

在每次与 GPT 进行交互后，检查响应中的 `finish_reason` 来确定对话是否应该结束。

```python
finish_reason = response['choices'][0]['finish_reason']
```

#### 2. 结束对话或继续交互

- 如果 `finish_reason` 为 'stop'，则表示对话已自然结束，此时可以直接将 GPT 的响应返回给用户。
- 如果 `finish_reason` 不是 'stop'，则可以继续与 GPT 交互，例如调用更多的函数或进一步与用户进行对话。

```python
if finish_reason == 'stop':
    return response_message['content']
```

## 总结

通过这种方式，用户可以利用 GPT 的函数调用特性来在一个连续的对话流程中实现多任务处理，例如获取天气信息并将结果保存到文件。同时，通过监控 `finish_reason`，我们可以确保聊天或任务在适当的时候结束，优化用户体验和系统性能。这种方法不仅增强了聊天机器人的功能性，还提供了一种灵活而强大的方式来根据用户的需求定制响应和操作。
