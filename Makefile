.PHONY: build

build:
	# Create `build` directory if it doesn't exist
	@mkdir -p build

	# If not already cloned, clone then build the model runtime
	@if [ ! -d "build/llama.cpp" ]; then \
		git clone https://github.com/ggerganov/llama.cpp.git build/llama.cpp; \
		cd build/llama.cpp && make && cd -; \
	fi

	# Get weights, if not already downloaded
	@if [ ! -f "build/llama-2-7b-chat.Q4_K_M.gguf" ]; then \
			wget -O build/llama-2-7b-chat.Q4_K_M.gguf https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf; \
	fi

clean:
	rm -rf build
