import pytest
import torch
from hierarchicalmemory import HierarchicalMemory, create_hierarchicalmemory

class TestHierarchicalMemory:
    def test_init(self):
        m = HierarchicalMemory(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = HierarchicalMemory(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_hierarchicalmemory()
        assert isinstance(m, HierarchicalMemory)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
