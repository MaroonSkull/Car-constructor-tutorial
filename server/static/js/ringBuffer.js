let createRingBuffer = function(length) {
	let end = 0,	// write index
		start = 0,	// read index
		capacity = length,
		buffer = [];

	return {
		push : function(item) {
			buffer[end++] = item;
			end %= capacity;
			if (end == start) start = (start + 1) % capacity;
		},

		shift : function() {
			if (end === start)
				return false;

			if (buffer[start]) {
				res = buffer[start++];
				start %= capacity;
				return res;
			}
			return false;
		},

		clear : function() {
			start = end = 0;
			buffer = [];
		},

		isEmpty : function() {
			return start === end;
		}
	};
};