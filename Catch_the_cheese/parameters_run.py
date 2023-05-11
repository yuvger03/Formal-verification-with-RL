class ParametersRun:
    def __init__(self):
        self.size = 10
        self.useNusmv = 1
        self.num_steps_in_episode = 7
        self.start_point = 0
        self.score = 5

    def get_size(self):
        return self.size

    def get_score(self):
        return self.score

    def get_useNusmv(self):
        return self.useNusmv

    def get_num_steps_in_episode(self):
        return self.num_steps_in_episode

    def get_start_point(self):
        return self.start_point

    def get_start_point_model_checker(self):
        return self.start_point + self.num_steps_in_episode

    def set_use_Nuxmv(self, value):
        self.useNusmv = value

    def set_num_steps_in_episode(self, value):
        self.num_steps_in_episode = value

    def set_start_point(self, value):
        self.start_point = value

    def set_score(self, value):
        self.score = value

    def set_size(self, value):
        self.size = value

    def setNewParameters(self, size):
        factor = size / 10
        self.set_size(size)
        self.set_num_steps_in_episode(int(7 * factor))
