import numpy as np


class ClickDefinition:
    """
    Class used to initialize the click model using the input YAML file.
    """

    def __init__(self, click_states, init_state, list_size, no_states, batch_size, no_items, abs_state, var_dic):
        self._act_matrices = {}
        self._var_type = {}
        self._t0_fixed = {}

        self._click_states = click_states
        self._init_state = init_state
        self._list_size = list_size
        self._no_states = no_states
        self._batch_size = batch_size
        self._no_items = no_items
        self._abs_state = abs_state
        self._init_act_matrices(var_dic)

    @property
    def no_items(self):
        """
        Number of items distinguished by the model
        """
        return self._no_items

    @property
    def batch_size(self):
        """
        Batch size used during optimization (in # sessions)
        """
        return self._batch_size

    @property
    def var_type(self):
        """
        Type of each variable (currently implemented: session and item)
        """
        return self._var_type

    @property
    def click_states(self):
        """
        The state at which an item is clicked
        """
        return self._click_states

    @property
    def init_state(self):
        """
        Initial state of the model during the start of each session (always equals the click state)
        """
        return self._init_state

    @property
    def list_size(self):
        """
        SERP size
        """
        return self._list_size

    @property
    def no_states(self):
        """
        Number of states used to define the click model
        """
        return self._no_states

    @property
    def act_matrices(self):
        """
        A dictionary of activation matrices, one for each variable
        """
        return self._act_matrices

    @property
    def t0_fixed(self):
        """
        A dictionary of parameters being fixed from transition 0 to 1
        """
        return self._t0_fixed

    @property
    def absorbing_state(self):
        """
        The absorbing state
        """
        return self._abs_state

    def _init_click_states(self, click_state_lst):
        click_state_mat_lst = []
        for row_val in click_state_lst:
            click_state_mat_lst.append(np.array(row_val[1]))  # TODO: This assumes the rows are ordered

        return np.vstack(click_state_mat_lst)

    def _init_absorbing_state(self, abs_state_lst):
        abs_state_mat = []

        for row_val in abs_state_lst:
            abs_state_mat.append(tuple(row_val))
        return abs_state_mat

    def _init_act_matrices(self, act_mat_dic):
        # Initializes the activation matrices
        for key, d in act_mat_dic.items():
            self._act_matrices[key] = {}
            for mat_type in ('pos_mat', 'neg_mat', "fixed_mat"):
                if mat_type in d:
                    mat = d[mat_type]
                else:
                    mat = np.zeros((self._no_states, self._no_states))

                self._act_matrices[key][mat_type] = mat

            self._var_type[key] = d['var_type']
            if 't0_fixed' in d:
                self._t0_fixed[key] = d['t0_fixed']

    def _get_act_mat(self, d, matrix_type):
        if matrix_type not in d:
            mat = np.array([])
        else:
            mat = d[matrix_type]

        return mat

    def _init_act_mat(self, d):
        # Initialized a single activation matrix
        act_mat = np.zeros((self._no_states, self._no_states))

        for row_val in d:
            act_mat[row_val[0], :] = np.array(row_val[1])

        return act_mat






