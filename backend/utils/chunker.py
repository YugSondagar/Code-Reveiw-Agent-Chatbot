class CodeChunker:
    def __init__(self,chunk_size=2000,overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_code(self,code,language):
        """Split code into manageable chunks for analysis"""
        if language == 'python':
            return self._chunk_python(code)
        elif language in ['javascript','typescript','java','cpp','c','go','rust']:
            return self._chunk_curly_brace(code)
        else:
            return self._chunk_by_lines(code)
    
    def _chunk_python(self,code):
        """Chunk python code at function/class boundaries"""
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0

        i = 0
        while i<len(lines):
            line = lines[i]
            line_size = len(line)
            if line.strip().startswith(('def','class')):
                if current_chunk and current_size > self.chunk_size//2:
                    chunks.append('\n'.join(current_chunk))
                    overlap_lines = current_chunk[-min(5, len(current_chunk)):]

                    current_chunk = overlap_lines.copy()
                    current_size = sum(len(l) for l in overlap_lines)
            current_chunk.append(line)
            current_size += line_size

            if current_size >= self.chunk_size:
                chunks.append('\n'.join(current_chunk))
                overlap_lines = current_chunk[-min(5,len(current_chunk)):]
                current_chunk = overlap_lines.copy()
                current_size = sum(len(l) for l in overlap_lines)

            i+=1

            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            return chunks if chunks else [code]
    
    def _chunk_curly_brace(self,code):
        """Chunk C-Style languages at function boundaries"""
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        brace_count = 0
        current_size = 0

        for line in lines:
            current_chunk.append(line)
            current_size += len(line)

            brace_count += line.count('{')-line.count('}')

            if brace_count == 0 and current_size>self.chunk_size//2:
                chunks.append('\n'.join(current_chunk))
                overlap_lines = current_chunk[-min(3,len(current_chunk)):]
                current_chunk = overlap_lines.copy()
                current_size = sum(len(l) for l in overlap_lines)
            elif current_size>= self.chunk_size and brace_count <= 1:
                chunks.append('\n'.join(current_chunk))
                overlap_lines = current_chunk[-min(3,len(current_chunk)):]
                current_chunk = overlap_lines.copy()
                current_size = sum(len(l) for l in overlap_lines)
            
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks if chunks else [code]
    
    def _chunk_by_lines(self,code):
        """Simple line-based chunking for other languages"""
        lines = code.split('\n')
        chunks = []
        chunk_lines = []
        chunk_size = 0

        for line in lines:
            chunk_lines.append(line)
            chunk_size += len(line)

            if chunk_size >= self.chunk_size:
                chunks.append('\n'.join(chunk_lines))
                chunk_lines = chunk_lines[-3:]
                chunk_size = sum(len(l) for l in chunk_lines)
        
        if chunk_lines:
            chunks.append('\n'.join(chunk_lines))
        
        return chunks if chunks else [code]