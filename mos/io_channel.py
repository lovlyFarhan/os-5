

class IOChannel:
    input_buffer = {}
    output_buffer = {}


    def send_input(vm, input_stream):
        IOChannel.input_buffer[vm] = input_stream

    def get_input():
        return IOChannel.input_buffer.popitem()

    def send_output(vm, output_stream):
        IOChannel.output_buffer[vm] = output_stream

    def get_output():
        return IOChannel.output_buffer.popitem()
