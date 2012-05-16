

class IOChannel:
    input_buffer = {}
    output_buffer = {}
    input_waiting_queue = []

    def send_input(vm, input_stream):
        print(input_stream)
        IOChannel.input_buffer[vm] = input_stream

    def send_output(vm, output_stream):
        IOChannel.output_buffer[vm] = output_stream

    def get_output():
        return IOChannel.output_buffer.popitem()

    def send_input_request(vm):
        IOChannel.input_waiting_queue.append(vm)

    def rotate_iwq():
        if IOChannel.input_waiting_queue != []:
            IOChannel.input_waiting_queue.append(IOChannel.input_waiting_queue.pop(0))
            return False
        else:
            return True
