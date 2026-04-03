"""RAG (Retrieval-Augmented Generation) Service for document context."""

from typing import List, Dict, Optional
import json


class RAGService:
    """Service for document retrieval and context injection."""
    
    def __init__(self):
        """Initialize RAG service."""
        self.documents: Dict[str, Dict] = {}
        self.embeddings_index: Dict[str, List[float]] = {}
    
    def add_document(self, doc_id: str, content: str, metadata: Dict = None) -> None:
        """Add a document to the RAG knowledge base."""
        self.documents[doc_id] = {
            "content": content,
            "metadata": metadata or {},
            "chunks": self._chunk_document(content)
        }
    
    def _chunk_document(self, content: str, chunk_size: int = 500) -> List[str]:
        """Split document into chunks for better retrieval."""
        words = content.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            
            if current_size > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def search_documents(self, query: str, top_k: int = 3) -> List[str]:
        """
        Simple keyword search in documents.
        In production, use vector similarity search with embeddings.
        """
        query_words = set(query.lower().split())
        results = []
        
        for doc_id, doc_data in self.documents.items():
            content_lower = doc_data["content"].lower()
            match_count = sum(1 for word in query_words if word in content_lower)
            
            if match_count > 0:
                results.append((doc_id, doc_data["content"], match_count))
        
        # Sort by relevance (match count)
        results.sort(key=lambda x: x[2], reverse=True)
        
        # Return top K results
        return [result[1] for result in results[:top_k]]
    
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant context from documents for a query."""
        relevant_docs = self.search_documents(query, top_k)
        
        if not relevant_docs:
            return ""
        
        # Combine retrieved documents
        context = "\n\n".join(relevant_docs)
        return context
    
    def list_documents(self) -> List[Dict]:
        """List all documents in the knowledge base."""
        return [
            {
                "doc_id": doc_id,
                "metadata": doc_data["metadata"],
                "chunk_count": len(doc_data["chunks"])
            }
            for doc_id, doc_data in self.documents.items()
        ]
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from knowledge base."""
        if doc_id in self.documents:
            del self.documents[doc_id]
            return True
        return False


# Global RAG service instance
rag_service = RAGService()
