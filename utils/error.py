def mk_runtime_error(response):
    return f"""
                Runtime Error
                Message: {response.content.decode("utf-8")}
                Status Code: {response.status_code}
            """
