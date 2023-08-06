# GROMACS

class TestBenzene(BaseDatasetTest):
    @pytest.fixture(scope="class",
                    params = [(load_benzene, ('Coulomb', 'VDW'), (5, 16)),
                              ])
    def dataset(self, request):
        return super().dataset(request)

class TestABFE(BaseDatasetTest):
    @pytest.fixture(scope="class",
                    params = [(load_ABFE, ('complex', 'ligand'), (30, 20)),
                              ])
    def dataset(self, request):
        return super().dataset(request)


class TestLoadExpandedEnsembleCase1(BaseDatasetTest):
    @pytest.fixture(scope="class",
                    params = [(load_expanded_ensemble_case_1, ('AllStates', ), (1,)),
                              ])
    def dataset(self, request):
        return super().dataset(request)


class TestLoadExpandedEnsembleCase2(BaseDatasetTest):
    @pytest.fixture(scope="class",
                    params = [(load_expanded_ensemble_case_2, ('AllStates', ), (2,)),
                              ])
    def dataset(self, request):
        return super().dataset(request)


class TestLoadExpandedEnsembleCase3(BaseDatasetTest):
    @pytest.fixture(scope="class",
                    params = [(load_expanded_ensemble_case_3, ('AllStates', ), (32,)),
                              ])
    def dataset(self, request):
        return super().dataset(request)


## NAMD

class TestTyr2Ala(BaseDatasetTest):
    @pytest.fixture(scope="class",
                    params = [(load_tyr2ala, ('forward', 'backward'), (1, 1)),
                              ])
    def dataset(self, request):
        return super().dataset(request)

class TestIDWS(BaseDatasetTest):
    @pytest.fixture(scope="class",
                    params = [(load_idws, ('forward', ), (2,)),
                              ])
    def dataset(self, request):
        return super().dataset(request)


