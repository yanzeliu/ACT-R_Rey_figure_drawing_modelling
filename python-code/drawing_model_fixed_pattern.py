import copy
import math
import random
import numpy as np
from collections import Counter

import matplotlib.pyplot as plt

import actr
import line_stroke
import pickle

EXP_WINDOW_WIDTH = 1500
EXP_WINDOW_HEIGHT = 900
STIMLUS_XS = [1498, 1535, 1478, 1465, 946, 975, 968, 1403, 1402, 1401, 1382, 1384, 1573, 1565, 1058, 945, 972, 1198,
              1200, 1229, 1258, 1286, 983, 967, 1034, 1086, 1131, 1183, 1224, 945, 941, 965, 501, 508, 700, 485, 499,
              488, 489, 514, 506, 510, 526, 509, 611, 504, 623, 709, 705, 507, 507, 610, 697, 776, 859, 717, 1160, 402,
              366, 427]
STIMLUS_XE = [1481, 1516, 1552, 1548, 942, 1379, 1380, 1729, 1724, 1728, 1385, 1389, 1570, 1569, 1053, 944, 1356, 1290,
              1373, 1252, 1299, 1344, 1383, 1374, 1081, 1130, 1178, 1228, 1270, 941, 945, 1363, 919, 680, 700, 485, 683,
              488, 491, 925, 918, 916, 942, 584, 688, 594, 690, 708, 710, 692, 704, 939, 941, 933, 932, 1207, 1168, 408,
              453, 476]
STIMLUS_YS = [90, 85, 108, 131, 207, 65, 224, 223, 426, 621, 439, 246, 336, 441, 234, 403, 408, 354, 336, 359, 365, 390,
              423, 433, 498, 518, 538, 560, 584, 446, 636, 623, 622, 634, 742, 642, 759, 607, 410, 236, 425, 608, 225,
              339, 431, 515, 399, 349, 443, 518, 330, 259, 302, 335, 377, 692, 668, 428, 136, 261]
STIMLUS_YE = [161, 163, 111, 133, 61, 215, 226, 418, 424, 434, 615, 416, 413, 509, 364, 239, 242, 411, 335, 344, 344,
              346, 422, 615, 454, 473, 496, 516, 542, 614, 679, 624, 622, 746, 633, 749, 757, 433, 231, 413, 424, 435,
              223, 406, 514, 435, 339, 415, 510, 518, 329, 257, 299, 334, 373, 692, 725, 101, 138, 260]
LINE_TAG = ['hash', 'hash', 'hash', 'hash', 'fin', 'fin', 'box', 'nose', 'nose', 'nose', 'box', 'box', 'nose', 'nose',
            'brow', 'body', 'body', 'eye', 'eye', 'pupil', 'pupil', 'pupil', 'body', 'body', 'gill', 'gill', 'gill',
            'gill', 'gill', 'body', 'spike', 'box', 'box', 'rear', 'rear', 'rear', 'rear', 'box', 'box', 'body', 'body',
            'body', 'box', 'tail', 'tail', 'tail', 'tail', 'tail', 'tail', 'tail', 'tail', 'back', 'back', 'back',
            'back', 'spike', 'spike', 'arial', 'arial', 'arial', ]
LINE_TAG_SUB_ID = [2, 3, 1, 4, 1, 2, 2, 1, 3, 5, 6, 4, 2, 4, 1, 2, 3, 2, 1, 1, 2, 3, 5, 8, 1, 2, 3, 4, 5, 7, 1, 8, 7, 2,
                   3, 1, 4, 5, 3, 1, 4, 6, 1, 2, 6, 5, 3, 4, 7, 8, 1, 1, 2, 3, 4, 2, 3, 2, 1, 3, ]
EXP_RUN_TIME = 8000

EXP_TRIAL_NUM = 40

PIXELS_PER_VIEWING_ANGLE = 35
TOTAL_REFERENCE_NUM = 20

VIEWING_DISTANCE_INCH = 15
PIXELS_PER_INCH = 72
ACT_R_DEFAULT_PIXELS_PER_ANGLE = 19

MILLI_SECONDS_A_DAY = 86400000

MIN_LINE_EDGE_LENGTH = 10
MAX_LINE_NUM_PER_GROUP = 4

TRIAL_TYPE_DM = 'DelayedRecall'
TRIAL_TYPE_IM = 'ImmediateRecall'
TRIAL_TYPE_CP = 'Copy'
TRIAL_TYPE_TR = 'Trace'

ENABLE_BASE_LEVEL_DIFFERENCES = False

LINE_LENGTH_DIFFERENCE_THRESHOLD = 0.15
LINE_DISTANCE_THRESHOLD = 0.3

class FigureDrawingMdeol:

    def __init__(self):

        self.stim_window = None
        self.resp_window = None
        self.run_in_real_time = True
        self.task_type = None
        self.stim_ye = None
        self.stim_ys = None
        self.stim_xe = None
        self.stim_xs = None
        self.line_strokes = None
        self.line_stroke_dict = {}
        self.pattern_chunk_names = []
        self.pixels_per_angle = None
        self.test_line_id = []
        self.line_group_label_idx = 1
        self.line_in_groups = []
        self.current_line_slot_idx = 0
        self.current_ling_group_name = None
        self.pattern_stroke_num = dict(Counter(LINE_TAG))
        self.drawing_start_time_list = []
        self.drawing_end_time_list = []
        self.drawing_line_type_list = []
        self.line_symmetry_dict = {}
        self.figure_centre_top_y = None
        self.figure_centre_bottom_y = None
        self.figure_centre_left_x = None
        self.figure_centre_right_x = None
        self.line_connection_list = {}
        self.line_nearby_list = {}
        self.copy_window_offset = -EXP_WINDOW_HEIGHT
        # self.copy_window_offset = 2 * EXP_WINDOW_HEIGHT
        self.experiment_result = []

        # for get_furthest_pattern_line_location
        self.pre_tar_screen_x = None
        self.pre_tar_screen_y = None

        self.trial_type_label_sequence = (TRIAL_TYPE_DM, TRIAL_TYPE_TR, TRIAL_TYPE_CP, TRIAL_TYPE_IM)
        # self.trial_type_label_sequence = (TRIAL_TYPE_DM, TRIAL_TYPE_CP, TRIAL_TYPE_TR, TRIAL_TYPE_IM)

        # sequence for testing
        # self.trial_type_label_sequence = (TRIAL_TYPE_DM, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR, TRIAL_TYPE_TR)
        # self.trial_type_label_sequence = (TRIAL_TYPE_DM, TRIAL_TYPE_TR, TRIAL_TYPE_CP, TRIAL_TYPE_TR, TRIAL_TYPE_CP, TRIAL_TYPE_TR, TRIAL_TYPE_CP, TRIAL_TYPE_TR, TRIAL_TYPE_CP)
        self.current_trial_idx = 1

    def run_experiment(self, run_in_real_time, total_reference_count):
        self.run_in_real_time = run_in_real_time
        if not run_in_real_time:
            actr.set_parameter_value(':v', False)
            actr.set_parameter_value(':cmdt', False)

        actr.add_command("start-button-pressed", self.trial_start_button_func)
        actr.add_command("finish-button-pressed", self.trial_finish_button_func)
        actr.add_command("create-line-chunks", self.create_line_stroke_chunk)
        actr.add_command("add-recognisable-to-dm", self.put_recognisable_line_into_dm)
        actr.add_command("get-recognisable-lines-chunk", self.put_recognisable_lines_into_a_chunk)
        actr.add_command("identify-pattern-from-recognisable-lines", self.identify_patterns_from_line_group_chunk)
        actr.add_command("identify-pattern-given-line-stim", self.identify_patterns_given_current_location)
        actr.add_command("add-recognisable-lines-into-dm", self.add_recognisable_lines_into_dm)
        actr.add_command("get-next-line-group-chunk-slot", self.get_line_slot_from_line_group)
        actr.add_command("add-responded-line", self.add_responded_line_to_response_panel)
        actr.add_command("record-response-time", self.record_drawing_time)
        actr.add_command("record-response-type", self.record_response_line_type)
        actr.add_command("check-all-line-are-drawn", self.check_all_line_is_repreduced)
        actr.add_command("get-tar-line-stim-chunk", self.get_tar_line_stim_chunk_name)
        actr.add_command("get-visible-symmetry-line", self.get_symmetry_line_from_visible_lines)
        actr.add_command("get-location-label", self.get_location_label)
        actr.add_command("check-chunk-type", self.check_retrieved_chunk_group_or_line)
        actr.add_command("get-furthest-pattern-line-location", self.get_furthest_pattern_line_location)
        actr.add_command("get-next-pattern-line-location", self.get_next_pattern_line_location)
        actr.add_command("get-updated-root-chunk", self.attach_pattern_chunk_into_root_in_goal)
        actr.add_command("clear-tmp-goal-chunk-imaginal", self.clear_tmp_imaginal_buffer_chunk)
        actr.add_command("get-fixated-line-chunk", self.get_current_fixated_line_chunk_name)
        actr.add_command("get-line-end-point-location", self.get_line_end_location)
        actr.add_command("get-location-of-unreproduced-line", self.get_location_of_unreproduced_line)
        actr.add_command("get-next-pattern-line-name-copying", self.get_next_pattern_line_chunk_name_for_copying)
        actr.add_command("get-line-end-coord-copying", self.get_line_end_2_coord)
        actr.add_command("get-furthest-pattern-line-chunk", self.get_furthest_pattern_line_chunk_name)
        actr.add_command("update-visual-location-for-copying", self.update_visual_location_for_copying)
        actr.add_command("check_whether_pattern_is_copy_finished", self.check_whether_pattern_is_reproduce_finished)



        actr.add_command("update-line-reference-count", self.calculate_reference_count_base_on_location)
        actr.add_command("get-center-x", self.get_center_x_of_figure)
        actr.add_command("get-center-y", self.get_center_y_of_figure)
        actr.add_command("encode-pattern-by-label", self.create_pattern_chunk_with_label)
        actr.add_command("create-screen-location", self.create_screen_location)
        actr.add_command("get-line-slot", self.get_line_slot_base_on_imaginal)
        actr.add_command("get-line-location", self.get_line_location)
        actr.add_command("add-line-copying", self.draw_line_for_copying)

        actr.add_command("break-point", self.break_point_for_test)

        self.total_reference_count = total_reference_count

        actr.reset()

        self.stim_window = actr.open_exp_window("Experiment", visible=run_in_real_time, width=EXP_WINDOW_WIDTH,
                                                height=EXP_WINDOW_HEIGHT, x=self.copy_window_offset, y=self.copy_window_offset)
        self.resp_window = actr.open_exp_window("Response", visible=run_in_real_time, width=EXP_WINDOW_WIDTH,
                                                height=EXP_WINDOW_HEIGHT, x=0, y=0)

        self.add_before_trial_text_and_button()

        actr.install_device(self.stim_window)
        actr.install_device(self.resp_window)
        actr.start_hand_at_mouse()

        actr.run(EXP_RUN_TIME, run_in_real_time)

        actr.remove_command("start-button-pressed")
        actr.remove_command("create-line-chunks")
        actr.remove_command("add-recognisable-to-dm")
        actr.remove_command("get-recognisable-lines-chunk")
        actr.remove_command("identify-pattern-from-recognisable-lines")
        actr.remove_command("identify-pattern-given-line-stim")
        actr.remove_command("add-recognisable-lines-into-dm")
        actr.remove_command("get-next-line-group-chunk-slot")
        actr.remove_command("add-responded-line")
        actr.remove_command("record-response-time")
        actr.remove_command("record-response-type")
        actr.remove_command("check-all-line-are-drawn")
        actr.remove_command("get-tar-line-stim-chunk")
        actr.remove_command("get-visible-symmetry-line")
        actr.remove_command("get-location-label")
        actr.remove_command("check-chunk-type")
        actr.remove_command("get-furthest-pattern-line-location")
        actr.remove_command("get-next-pattern-line-location")
        actr.remove_command("get-updated-root-chunk")
        actr.remove_command("clear-tmp-goal-chunk-imaginal")
        actr.remove_command("get-fixated-line-chunk")
        actr.remove_command("get-line-end-point-location")
        actr.remove_command("get-location-of-unreproduced-line")
        actr.remove_command("get-next-pattern-line-name-copying")
        actr.remove_command("get-line-end-coord-copying")
        actr.remove_command("get-furthest-pattern-line-chunk")
        actr.remove_command("update-visual-location-for-copying")
        actr.remove_command("check_whether_pattern_is_copy_finished")


        actr.remove_command("update-line-reference-count")
        actr.remove_command("get-center-x")
        actr.remove_command("get-center-y")
        actr.remove_command("encode-pattern-by-label")
        actr.remove_command("create-screen-location")
        actr.remove_command("get-line-slot")
        actr.remove_command("get-line-location")
        actr.remove_command("add-line-copying")
        actr.remove_command("break-point")

    def add_before_trial_text_and_button(self):
        actr.add_text_to_exp_window(self.stim_window, text=self.trial_type_label_sequence[self.current_trial_idx],
                                    x=EXP_WINDOW_WIDTH / 2, y=EXP_WINDOW_HEIGHT / 2, font_size=25)
        actr.add_button_to_exp_window(self.stim_window, text="Start", x=EXP_WINDOW_WIDTH / 2, y=EXP_WINDOW_HEIGHT - 100,
                                      action="start-button-pressed",
                                      height=24, width=65)
        self.current_trial_idx = (self.current_trial_idx + 1) % len(self.trial_type_label_sequence)

    def trial_start_button_func(self):
        actr.clear_exp_window(self.stim_window)
        actr.clear_exp_window(self.resp_window)


        task_type = self.trial_type_label_sequence[(self.current_trial_idx - 1) % len(self.trial_type_label_sequence)]
        if task_type == TRIAL_TYPE_TR:
            self.add_tracing_stimulus_to_screen()
        elif task_type == TRIAL_TYPE_CP:
            self.add_copying_stimulus_to_screen()
        self.task_type = task_type

        actr.add_button_to_exp_window(self.resp_window, text="Finish", x=EXP_WINDOW_WIDTH / 2,
                                      y=EXP_WINDOW_HEIGHT - 100,
                                      action="finish-button-pressed",
                                      height=24, width=65)

        # self.add_tracing_stimulus_to_screen()
        # self.add_copying_stimulus_to_screen()
        # self.define_line_tag_as_chunk()

    def trial_finish_button_func(self):
        # print('finish button pressed')
        # print(self.drawing_start_time_list)
        # print(self.drawing_end_time_list)
        # if self.current_trial_idx > 4:
        #     print('test')
        print(self.drawing_line_type_list)
        a = self.drawing_line_type_list
        self.record_experiment_data()
        self.reset_model_setting()

        if len(self.experiment_result) == EXP_TRIAL_NUM:
            return

        actr.clear_exp_window(self.stim_window)
        actr.clear_exp_window(self.resp_window)
        self.add_before_trial_text_and_button()

        if self.task_type == TRIAL_TYPE_IM:
            self.update_chunk_creation_time()

        if self.line_strokes is not None:
            for line_stim in self.line_strokes:
                line_stim.reproduced = False

    def update_chunk_creation_time(self):
        for line_stim in self.line_strokes:
            creation_time = actr.get_chunk_creation_time(line_stim.chunk_name)
            actr.set_creation_time(line_stim.chunk_name, creation_time - MILLI_SECONDS_A_DAY)

        line_group_chunk_name = actr.sdm("chunk-type-tag", "line-group")
        for chunk_name in line_group_chunk_name:
            creation_time = actr.get_chunk_creation_time(chunk_name)
            actr.set_creation_time(line_stim.chunk_name, creation_time - MILLI_SECONDS_A_DAY)

    def reset_model_setting(self):
        self.drawing_start_time_list = []
        self.drawing_end_time_list = []
        self.drawing_line_type_list = []
        self.pre_tar_screen_x = None
        self.pre_tar_screen_y = None
        actr.reset_declarative_finsts()
        actr.remove_visual_finsts()

    def record_experiment_data(self):
        self.experiment_result.append((self.drawing_start_time_list, self.drawing_end_time_list,self.drawing_line_type_list, self.task_type))

    def add_copying_stimulus_to_screen(self):
        # resize stimulus
        # self.stim_xs = list(np.array(STIMLUS_XS) / 2)
        # self.stim_xe = list(np.array(STIMLUS_XE) / 2)
        # self.stim_ys = list(np.array(STIMLUS_YS) / 2)
        # self.stim_ye = list(np.array(STIMLUS_YE) / 2)

        self.stim_xs = list(np.array(STIMLUS_XS, dtype=np.float64) - 300)
        self.stim_xe = list(np.array(STIMLUS_XE, dtype=np.float64) - 300)
        self.stim_ys = list(np.array(STIMLUS_YS, dtype=np.float64))
        self.stim_ye = list(np.array(STIMLUS_YE, dtype=np.float64))
        for xs, xe, ys, ye in zip(self.stim_xs, self.stim_xe, self.stim_ys, self.stim_ye):
            line_id = actr.add_line_to_exp_window(self.stim_window, [xs, ys], [xe, ye], ["blue"])

            # actr.add_visicon_features(['screen-x', 0, 'screen-y', 5, 'regular', 'true'])
            # print(line_id)

    def add_tracing_stimulus_to_screen(self):
        # move stimulus to left
        self.stim_xs = list(np.array(STIMLUS_XS, dtype=np.float64) - 300)
        self.stim_xe = list(np.array(STIMLUS_XE, dtype=np.float64) - 300)
        self.stim_ys = list(np.array(STIMLUS_YS, dtype=np.float64))
        self.stim_ye = list(np.array(STIMLUS_YE, dtype=np.float64))
        for xs, xe, ys, ye in zip(self.stim_xs, self.stim_xe, self.stim_ys, self.stim_ye):
            line_id = actr.add_line_to_exp_window(self.resp_window, [xs, ys], [xe, ye], ["blue"])
            # test = actr.modify_line_for_exp_window(line_id, [xs, ys], [xe, ye], ["black"])
            # print(test)

    # def define_line_tag_as_chunk(self):
    #     for idx in range(len(self.stim_xs)):
    #         actr.define_chunks('line-' + str(idx + 1))

    def create_line_stroke_chunk(self):
        if self.line_strokes is not None:
            return

        visicon_str = actr.printed_visicon()
        visicon_content_arr = list(
            filter(lambda x: ("LINE" in x) & x.startswith("VISUAL-LOCATION"), visicon_str.split('\n')))
        self.line_num = len(visicon_content_arr)

        # create disc chunks and store the names of those chunks
        self.line_chunk_names = []
        self.line_strokes = []
        line_stim_chunk_param_list = []
        for loc_str in visicon_content_arr:
            location_str = loc_str[loc_str.index('(') + 1:loc_str.index(')')].strip()
            coord_arr = location_str.split()
            coord_x = int(coord_arr[0])
            coord_y = int(coord_arr[1])
            line_number_str = loc_str.split()[0]
            line_number_str = line_number_str[line_number_str.index('N') + 1:]

            # line_label_str = 'line-label-' + line_number_str

            line_coords = loc_str.split()[-4:]
            line_color = loc_str[loc_str.index(' "') + 2:loc_str.index('" ')].strip()

            # actr.define_chunks(line_label_str)
            # tmp_chunk_name = actr.define_chunks(
            #     ['isa', 'line-stimulus', 'color', line_color, 'label', line_label_str, 'screen-x', coord_x, 'screen-y',
            #      coord_y, 'x-s', line_coords[3], 'y-s', line_coords[2], 'x-e', line_coords[1], 'y-e', line_coords[0]])[
            #     0]
            # tmp_line_obj = line_stroke.LineStroke(coord_x, coord_y, int(line_coords[3]), int(line_coords[2]),
            #                                       int(line_coords[1]), int(line_coords[0]), tmp_chunk_name)

            tmp_line_obj = line_stroke.LineStroke(coord_x, coord_y, int(line_coords[3]), int(line_coords[2]),
                                                  int(line_coords[1]), int(line_coords[0]))
            line_stim_chunk_param_list.append(['isa', 'line-stimulus', 'color', line_color, 'screen-x', coord_x, 'screen-y',
                 coord_y, 'x-s', line_coords[3], 'y-s', line_coords[2], 'x-e', line_coords[1], 'y-e', line_coords[0]])
            # tmp_line_obj.label_slot_value = line_label_str
            self.line_strokes.append(tmp_line_obj)
            # self.line_chunk_names.append(tmp_chunk_name)

        self.calculate_line_size()
        self.label_line_stroke_with_type_tag()
        self.get_figure_centre_border_coordinates()


        # create line-stimulus chunks
        for i in range(len(line_stim_chunk_param_list)):
            location_label = self.get_location_tag(self.line_strokes[i].screen_x, self.line_strokes[i].screen_y)
            line_stim_chunk_param_list[i].extend(['location', location_label])
            line_stim_chunk_param_list[i].extend(['label', self.line_strokes[i].type_tag])
            line_stim_chunk_param_list[i].extend(['type', 'line-' + self.line_strokes[i].type_tag])
            tmp_chunk_name = actr.define_chunks(line_stim_chunk_param_list[i])[0]
            self.line_chunk_names.append(tmp_chunk_name)
            self.line_strokes[i].chunk_name = tmp_chunk_name
            self.line_stroke_dict[tmp_chunk_name] = self.line_strokes[i]

        self.get_line_symmetry_for_all_line_strokes()
        # self.get_continuing_line_for_each_line_stroke()
        self.get_continuing_lines_using_interaction()

        # self.test_show_all_symetric_line_of_each_line()
        # self.test_find_tar_lines_using_tag()

    def calculate_line_size(self):
        for line_stim in self.line_strokes:
            # width_in_pixels = max(MIN_LINE_EDGE_LENGTH, abs(line_stim.x_e - line_stim.x_s))
            # hight_in_pixels = max(MIN_LINE_EDGE_LENGTH, abs(line_stim.y_e - line_stim.y_s))
            # height_inch = hight_in_pixels / PIXELS_PER_INCH
            # width_inch = width_in_pixels / PIXELS_PER_INCH
            # height_in_angle = math.degrees(2 * math.atan(height_inch / 2 / VIEWING_DISTANCE_INCH))
            # width_in_angle = math.degrees(2 * math.atan(width_inch / 2 / VIEWING_DISTANCE_INCH))
            # line_stim.size = width_in_angle * height_in_angle

            circle_diameter_in_pixels = math.sqrt(
                ((line_stim.x_e - line_stim.x_s) ** 2) + ((line_stim.y_e - line_stim.y_s) ** 2))
            circle_diameter_in_inch = circle_diameter_in_pixels / PIXELS_PER_INCH
            circle_diameter_in_angle = math.degrees(2 * math.atan(circle_diameter_in_inch / 2 / VIEWING_DISTANCE_INCH))
            line_stim.size = math.pi * ((circle_diameter_in_angle / 2) ** 2)

    def label_line_stroke_with_type_tag(self):
        x_s_np = np.array(self.stim_xs)
        y_s_np = np.array(self.stim_ys)
        x_e_np = np.array(self.stim_xe)
        y_e_np = np.array(self.stim_ye)
        for line_stim in self.line_strokes:
            xs_idx = np.where(abs(x_s_np - line_stim.x_s) < 1)[0]
            ys_idx = np.where(abs(y_s_np - line_stim.y_s) < 1)[0]
            xe_idx = np.where(abs(x_e_np - line_stim.x_e) < 1)[0]
            ye_idx = np.where(abs(y_e_np - line_stim.y_e) < 1)[0]
            con_arr = np.concatenate((xs_idx, ys_idx, xe_idx, ye_idx), axis=0)

            unique_rtn = np.unique(con_arr, return_counts=True)
            if np.where(np.max(unique_rtn[1]) == unique_rtn[1]).__len__() > 1:
                # deal with miss matching
                print(np.where(np.max(unique_rtn[1]) == unique_rtn[1]))
            max_counts_idx = np.argmax(unique_rtn[1])
            max_tag_idx = unique_rtn[0][max_counts_idx]
            line_stim.type_tag = LINE_TAG[max_tag_idx]

    # def get_projected_y_coord_for_copying(self, ):

    def get_nearby_patterns(self, line_stim):
        nearby_pattern_list = []
        for line_stim_key in self.line_stroke_dict.keys():
            if line_stim_key == line_stim.chunk_name:
                continue
            line_stim_tmp = self.line_stroke_dict[line_stim_key]
            if abs(line_stim.screen_x - line_stim_tmp.screen_x) < 5 and abs(line_stim.screen_y - line_stim_tmp.screen_y) < 5:
                nearby_pattern_list.append(line_stim_tmp)
        return nearby_pattern_list

    def get_continuing_line_for_each_line_stroke(self):

        # create adjacency list
        self.line_connection_list = dict((el.chunk_name, []) for el in self.line_strokes)
        for i in range(len(self.line_strokes)):
            for j in range(i + 1, len(self.line_strokes)):
                line_i = self.line_strokes[i]
                line_j = self.line_strokes[j]
                # if line_i.type_tag == 'box' and line_j.type_tag == 'box':
                #     print(line_i)

                end_distance_1 = np.linalg.norm(np.array([line_i.x_e, line_i.y_e]) - np.array([line_j.x_e, line_j.y_e]))
                end_distance_2 = np.linalg.norm(np.array([line_i.x_e, line_i.y_e]) - np.array([line_j.x_s, line_j.y_s]))
                end_distance_3 = np.linalg.norm(np.array([line_i.x_s, line_i.y_s]) - np.array([line_j.x_e, line_j.y_e]))
                end_distance_4 = np.linalg.norm(np.array([line_i.x_s, line_i.y_s]) - np.array([line_j.x_s, line_j.y_s]))
                min_end_distance = min(end_distance_1, end_distance_2, end_distance_3, end_distance_4)

                line_i_length = np.linalg.norm(np.array([line_i.x_s, line_i.y_s]) - np.array([line_i.x_e, line_i.y_e]))
                line_j_length = np.linalg.norm(np.array([line_j.x_s, line_j.y_s]) - np.array([line_j.x_e, line_j.y_e]))
                min_line_length = min(line_i_length, line_j_length)

                if min_end_distance < min_line_length * 0.15:
                    self.line_connection_list[line_i.chunk_name].append(copy.deepcopy(line_j))
                    self.line_connection_list[line_j.chunk_name].append(copy.deepcopy(line_i))

        # self.test_show_all_linked_line_of_each_line()
        print(self.line_connection_list)


    def get_continuing_lines_using_interaction(self):
        self.line_connection_list = dict((el.chunk_name, []) for el in self.line_strokes)
        for i in range(len(self.line_strokes)):
            for j in range(i + 1, len(self.line_strokes)):
                line_i = self.line_strokes[i]
                line_j = self.line_strokes[j]

                end_distance_1 = np.linalg.norm(np.array([line_i.x_e, line_i.y_e]) - np.array([line_j.x_e, line_j.y_e]))
                end_distance_2 = np.linalg.norm(np.array([line_i.x_e, line_i.y_e]) - np.array([line_j.x_s, line_j.y_s]))
                end_distance_3 = np.linalg.norm(np.array([line_i.x_s, line_i.y_s]) - np.array([line_j.x_e, line_j.y_e]))
                end_distance_4 = np.linalg.norm(np.array([line_i.x_s, line_i.y_s]) - np.array([line_j.x_s, line_j.y_s]))
                min_end_distance = min(end_distance_1, end_distance_2, end_distance_3, end_distance_4)

                line_i_length = np.linalg.norm(np.array([line_i.x_s, line_i.y_s]) - np.array([line_i.x_e, line_i.y_e]))
                line_j_length = np.linalg.norm(np.array([line_j.x_s, line_j.y_s]) - np.array([line_j.x_e, line_j.y_e]))
                min_line_length = min(line_i_length, line_j_length)

                # deal with parallel situations first
                if (line_i.vertical and line_j.vertical):
                    if abs(line_i.x_s - line_j.x_s) < 5 and min_end_distance < min_line_length * LINE_DISTANCE_THRESHOLD:
                        self.line_connection_list[line_i.chunk_name].append(copy.deepcopy(line_j))
                        self.line_connection_list[line_j.chunk_name].append(copy.deepcopy(line_i))
                elif (line_i.horizontal and line_j.horizontal):
                    if abs(line_i.y_s - line_j.y_s) < 5 and min_end_distance < min_line_length * LINE_DISTANCE_THRESHOLD:
                        self.line_connection_list[line_i.chunk_name].append(copy.deepcopy(line_j))
                        self.line_connection_list[line_j.chunk_name].append(copy.deepcopy(line_i))
                else:
                    # if (line_i.type_tag == 'body' and line_j.type_tag == 'back') or (line_i.type_tag == 'back' and line_j.type_tag == 'body'):
                    #     if line_j.screen_y == 321:
                    #         print(line_i.type_tag, line_i.vertical,  line_i.screen_y, line_j.type_tag, line_j.vertical,  line_j.screen_y)
                    intersect_point = np.array(line_intersection(([line_i.x_e, line_i.y_e], [line_i.x_s, line_i.y_s]), ([line_j.x_e, line_j.y_e], [line_j.x_s, line_j.y_s])))

                    # check the intersect point is not on either of the two lines
                    if point_on_segment(intersect_point, [[line_i.x_s, line_i.y_s], [line_i.x_e, line_i.y_e]]) or\
                            point_on_segment(intersect_point, [[line_j.x_s, line_j.y_s], [line_j.x_e, line_j.y_e]]):
                        continue

                    intersect_line_i_distance = min(np.linalg.norm(np.array([line_i.x_e, line_i.y_e]) - intersect_point), np.linalg.norm(np.array([line_i.x_s, line_i.y_s]) - intersect_point))
                    intersect_line_j_distance = min(np.linalg.norm(np.array([line_j.x_e, line_j.y_e]) - intersect_point), np.linalg.norm(np.array([line_j.x_s, line_j.y_s]) - intersect_point))
                    if intersect_line_i_distance < min_line_length * LINE_DISTANCE_THRESHOLD and intersect_line_j_distance < min_line_length * LINE_DISTANCE_THRESHOLD:
                        self.line_connection_list[line_i.chunk_name].append(copy.deepcopy(line_j))
                        self.line_connection_list[line_j.chunk_name].append(copy.deepcopy(line_i))

        # self.test_show_all_linked_line_of_each_line()
        # print(self.line_connection_list)

    def get_nearby_lines_for_each_line_stroke(self):
        line_nearby_list = dict((el, []) for el in range(len(STIMLUS_XS)))

        stim_xs = np.array(STIMLUS_XS)
        stim_ys = np.array(STIMLUS_YS)
        stim_xe = np.array(STIMLUS_XE)
        stim_ye = np.array(STIMLUS_YE)
        for i in range(len(stim_xs)):
            for j in range(i + 1, len(stim_xs)):
                line1 = np.array([[stim_xs[i], stim_ys[i]], [stim_xe[i], stim_ye[i]]])
                line2 = np.array([[stim_xs[j], stim_ys[j]], [stim_xe[j], stim_ye[j]]])
                grid1 = np.mgrid[min(line1[0][0], line1[1][0]):max(line1[0][0], line1[1][0]) + 1,
                        min(line1[0][1], line1[1][1]):max(line1[0][1], line1[1][1]) + 1]
                grid2 = np.mgrid[min(line2[0][0], line2[1][0]):max(line2[0][0], line2[1][0]) + 1,
                        min(line2[0][1], line2[1][1]):max(line2[0][1], line2[1][1]) + 1]

                points1 = np.vstack((grid1[0].flatten(), grid1[1].flatten())).T
                points2 = np.vstack((grid2[0].flatten(), grid2[1].flatten())).T

                # Calculate pairwise distances
                distances = np.linalg.norm(points1[:, np.newaxis] - points2, axis=-1)

                min_distance = np.min(distances)


    def get_line_symmetry_for_all_line_strokes(self):
        for line_stim in self.line_strokes:
            # if line is vertical
            if line_stim.x_s == line_stim.x_e:
                line_stim.slope = None
                line_stim.intercept = None
                line_stim.vertical = True
            else:
                # calculate the slope and intercept of the line
                line_stim.slope = (line_stim.y_e - line_stim.y_s) / (line_stim.x_e - line_stim.x_s)
                line_stim.intercept = line_stim.y_s - line_stim.slope * line_stim.x_s

                # label line within tolerated range as vertical
                if abs(math.degrees(math.atan(line_stim.slope))) < 10:
                    line_stim.horizontal = True
                # label line within tolerated range as horizontal
                elif abs(math.degrees(math.atan(line_stim.slope))) > 80:
                    line_stim.vertical = True

        #         print(line_stim.type_tag, line_stim.vertical, line_stim.horizontal, math.degrees(math.atan(line_stim.slope)), line_stim.intercept)


        self.line_symmetry_dict = dict((el.chunk_name, []) for el in self.line_strokes)
        # pair wise check line has same slope and intercept
        for i in range(len(self.line_strokes)):
            for j in range(i + 1, len(self.line_strokes)):
                line_i = self.line_strokes[i]
                line_j = self.line_strokes[j]

                # check if two lines are both vertical and same length
                if line_i.vertical and line_j.vertical:
                    line_i_length = abs(line_i.y_e - line_i.y_s)
                    line_j_length = abs(line_j.y_e - line_j.y_s)
                    len_diff_threshold = min(line_i_length, line_j_length) * LINE_LENGTH_DIFFERENCE_THRESHOLD
                    if abs(line_i_length - line_j_length) < len_diff_threshold:
                        if abs(line_i.screen_y - line_j.screen_y) < len_diff_threshold or abs(
                                line_i.screen_x - line_j.screen_x) < len_diff_threshold:
                            self.line_symmetry_dict[line_i.chunk_name].append(copy.deepcopy(line_j))
                            self.line_symmetry_dict[line_j.chunk_name].append(copy.deepcopy(line_i))
                            # self.test_show_symetric_line([line_j, line_i])

                # check if two lines are both horizontal and same length
                elif line_i.horizontal and line_j.horizontal:
                    line_i_length = abs(line_i.x_e - line_i.x_s)
                    line_j_length = abs(line_j.x_e - line_j.x_s)
                    len_diff_threshold = min(line_i_length, line_j_length) * LINE_LENGTH_DIFFERENCE_THRESHOLD
                    if abs(line_i_length - line_j_length) < len_diff_threshold:
                        if abs(line_i.screen_y - line_j.screen_y) < len_diff_threshold or abs(
                                line_i.screen_x - line_j.screen_x) < len_diff_threshold:
                            self.line_symmetry_dict[line_i.chunk_name].append(copy.deepcopy(line_j))
                            self.line_symmetry_dict[line_j.chunk_name].append(copy.deepcopy(line_i))
                            # self.test_show_symetric_line([line_j, line_i])

                elif not line_i.vertical and not line_j.vertical and not line_i.horizontal and not line_j.horizontal:

                    line_i_length = math.sqrt((line_i.x_e - line_i.x_s) ** 2 + (line_i.y_e - line_i.y_s) ** 2)
                    line_j_length = math.sqrt((line_j.x_e - line_j.x_s) ** 2 + (line_j.y_e - line_j.y_s) ** 2)
                    len_diff_threshold = min(line_i_length, line_j_length) * LINE_LENGTH_DIFFERENCE_THRESHOLD

                    if abs(line_i_length - line_j_length) < len_diff_threshold:
                        # if two lines are parallel
                        if abs(math.degrees(math.atan(line_i.slope)) - math.degrees(math.atan(line_j.slope))) < 5:
                            self.line_symmetry_dict[line_i.chunk_name].append(copy.deepcopy(line_j))
                            self.line_symmetry_dict[line_j.chunk_name].append(copy.deepcopy(line_i))
                            # self.test_show_symetric_line([line_j, line_i])
                        else:
                            # get the intersection point of the two lines
                            x_intersect = (line_j.intercept - line_i.intercept) / (line_i.slope - line_j.slope)
                            y_intersect = line_i.slope * x_intersect + line_i.intercept
                            intersect_point = np.array([x_intersect, y_intersect])

                            intersect_line_i_dis = np.linalg.norm(intersect_point - np.array([line_i.screen_x, line_i.screen_y]))
                            intersect_line_j_dis = np.linalg.norm(intersect_point - np.array([line_j.screen_x, line_j.screen_y]))
                            if abs(intersect_line_i_dis - intersect_line_j_dis) < len_diff_threshold:
                                self.line_symmetry_dict[line_i.chunk_name].append(copy.deepcopy(line_j))
                                self.line_symmetry_dict[line_j.chunk_name].append(copy.deepcopy(line_i))
                                # self.test_show_symetric_line([line_j, line_i])

        # =========================================================
        # test code
        # =========================================================
        # print(self.line_symmetry_dict)
        # tar_lines = []
        # for line_stim in self.line_strokes:
        #     if line_stim.type_tag == 'gill':
        #         tar_lines.append(line_stim)
        #         print(math.degrees(math.atan(line_stim.slope)), (line_stim.x_e - line_stim.x_s) , (line_stim.y_e - line_stim.y_s))
        # print(tar_lines)

    def get_symmetry_line_from_visible_lines(self, visual_location, goal_chunk):
        fovea_x = actr.chunk_slot_value(visual_location, 'screen-x')
        fovea_y = actr.chunk_slot_value(visual_location, 'screen-y')

        # get line chunk name currently fixated
        fixated_line_chunk_name = None
        for line_stim in self.line_strokes:
            if line_stim.screen_x == fovea_x and line_stim.screen_y == fovea_y:
                fixated_line_chunk_name = line_stim.chunk_name
                break

        recognisable_line_arr = self.calculate_line_visibility(fovea_x, fovea_y)
        visible_line_chunk_names = set(el.chunk_name for el in recognisable_line_arr)
        symmetry_line_chunk_names = set(el.chunk_name for el in self.line_symmetry_dict[fixated_line_chunk_name])
        tar_line_chunk_names = visible_line_chunk_names.intersection(symmetry_line_chunk_names)
        tar_line_chunk_names.add(fixated_line_chunk_name)

        # Create line group chunk ??
        chunk_param_list = ['isa', 'line-group']
        cur_slot_idx = 1
        for chunk_name in tar_line_chunk_names:
            chunk_param_list.append('line' + str(cur_slot_idx))
            chunk_param_list.append(chunk_name)
            cur_slot_idx += 1
        line_group_chunk_name = actr.define_chunks(chunk_param_list)[0]
        actr.add_dm_chunks(line_group_chunk_name)

        # attach to corresponding location slot in goal chunk
        location_slot_name = self.get_location_label(visual_location)

        location_slot_content_chunk_name = actr.chunk_slot_value(goal_chunk, location_slot_name)
        # print(location_slot_content_chunk_name)
        location_chunk_slots = self.get_chunk_slot_values(location_slot_content_chunk_name)

        for slot_value_pair in location_chunk_slots:
            # chunk_param_list.append('line' + str(cur_slot_idx))
            chunk_param_list.append(slot_value_pair[0])
            chunk_param_list.append(slot_value_pair[1])

        cur_slot_idx = len(location_chunk_slots) + 1
        chunk_param_list.append('line' + str(cur_slot_idx))
        chunk_param_list.append(line_group_chunk_name)
        new_slot_content_chunk_name = actr.define_chunks(chunk_param_list)[0]
        # actr.set_chunk_slot_value(goal_chunk, location_slot_name, new_slot_content_chunk_name)
        return new_slot_content_chunk_name

    def get_location_label(self, visual_location):
        fovea_x = actr.chunk_slot_value(visual_location, 'screen-x')
        fovea_y = actr.chunk_slot_value(visual_location, 'screen-y')

        # location_slot_name = None
        # if fovea_x < self.figure_centre_left_x:
        #     location_slot_name = 'figure-left'
        # elif fovea_x > self.figure_centre_right_x:
        #     location_slot_name = 'figure-right'
        # elif fovea_y < self.figure_centre_top_y and self.figure_centre_left_x <= fovea_x <= self.figure_centre_right_x:
        #     location_slot_name = 'figure-top'
        # elif fovea_y > self.figure_centre_bottom_y:
        #     location_slot_name = 'figure-bottom'
        # else:
        #     location_slot_name = 'figure-centre'
        #
        # return location_slot_name
        return self.get_location_tag(fovea_x, fovea_y)

    def get_location_tag(self, x, y):

        location_tag = None
        if x < self.figure_centre_left_x:
            location_tag = 'figure-left'
        elif x > self.figure_centre_right_x:
            location_tag = 'figure-right'
        elif y < self.figure_centre_top_y and self.figure_centre_left_x <= y <= self.figure_centre_right_x:
            location_tag = 'figure-top'
        elif y > self.figure_centre_bottom_y:
            location_tag = 'figure-bottom'
        else:
            location_tag = 'figure-centre'

        return location_tag

    def check_retrieved_chunk_group_or_line(self, chunk_name):
        label_str = actr.chunk_slot_value(chunk_name, 'type')
        # check label_str whether startwith line or group
        if label_str is None:
            return 'other'

        if label_str.startswith('LINE'):
            return 'line'
        elif label_str.startswith('GROUP'):
            return 'group'
        return 'other'


    def get_figure_centre_border_coordinates(self):
        x_coordinates = []
        y_coordinates = []
        for line_stim in self.line_strokes:
            if line_stim.type_tag == 'box':
                x_coordinates.append(line_stim.x_e)
                x_coordinates.append(line_stim.x_s)
                y_coordinates.append(line_stim.y_e)
                y_coordinates.append(line_stim.y_s)

        self.figure_centre_top_y = min(y_coordinates)
        self.figure_centre_bottom_y = max(y_coordinates)
        self.figure_centre_left_x = min(x_coordinates)
        self.figure_centre_right_x = max(x_coordinates)



    def calculate_line_visibility(self, fovea_x, fovea_y):
        # Equation: threshold = 0.3 (e ** 2) + 0.1 e + 0.1
        #           X ~ N (0.7 * s)
        pixel_per_viewing_angle = self.calculate_pixel_per_viewing_angle()
        recognisable_line_arr = []
        for line_stim in self.line_strokes:
            eccentricity = math.sqrt(
                (line_stim.screen_x - fovea_x) ** 2 + (line_stim.screen_y - fovea_y) ** 2) / pixel_per_viewing_angle
            threshold_shape = 0.3 * (eccentricity ** 2) + 0.1 * eccentricity + 0.1
            # threshold_shape = 10.3 * (eccentricity ** 2) + 0.1 * eccentricity + 0.1
            gaussian_noise = random.gauss(0, 0.7 * line_stim.size)
            if line_stim.size >= threshold_shape + gaussian_noise:
                line_stim.eccentricity = eccentricity
                recognisable_line_arr.append(line_stim)

        return recognisable_line_arr

    def put_recognisable_lines_into_a_chunk(self, visual_location, cur_chunk = None):

        fovea_x = actr.chunk_slot_value(visual_location, 'screen-x')
        fovea_y = actr.chunk_slot_value(visual_location, 'screen-y')

        print(visual_location, fovea_x, fovea_y, "put_recognisable_lines_into_a_chunk")

        # get original content of imaginal buffer
        # imaginal_buffer_content = actr.buffer_chunk('imaginal')
        # tar_line = actr.chunk_slot_value('line20')
        slot_chunk_name_pair = []
        if cur_chunk is not None:
            slot_chunk_name_pair = self.get_chunk_slot_values(cur_chunk)
            if 'LABEL' in set(el[0] for el in slot_chunk_name_pair):
                slot_chunk_name_pair = []
        line_chunk_name_list = list(el[1] for el in slot_chunk_name_pair)

        recognisable_line_arr = self.calculate_line_visibility(fovea_x, fovea_y)
        # Create temp line groups chunk
        chunk_param_list = ['isa', 'line-group']

        cur_slot_idx = 1
        for slot_value_pair in slot_chunk_name_pair:
            chunk_param_list.append('line' + str(cur_slot_idx))
            chunk_param_list.append(slot_value_pair[1])
            cur_slot_idx += 1

        for idx, line_stim in enumerate(recognisable_line_arr):
            if line_stim.chunk_name in line_chunk_name_list:
                continue
            chunk_param_list.append('line' + str(cur_slot_idx))
            chunk_param_list.append(line_stim.chunk_name)
            cur_slot_idx += 1

        tmp_chunk_name = actr.define_chunks(chunk_param_list)[0]
        # actr.set_buffer_chunk('imaginal', tmp_chunk_name)

        for line_stim in recognisable_line_arr:
            # actr.add_dm_chunks(line_stim.chunk_name)
            actr.merge_dm_chunks(line_stim.chunk_name)
            # print(line_stim.chunk_name)
        for slot_value_pair in slot_chunk_name_pair:
            # actr.add_dm_chunks(slot_value_pair[1])
            actr.merge_dm_chunks(slot_value_pair[1])
            # print(slot_value_pair[1])

        return tmp_chunk_name

    def add_recognisable_lines_into_dm(self, visual_location):
        fovea_x = actr.chunk_slot_value(visual_location, 'screen-x')
        fovea_y = actr.chunk_slot_value(visual_location, 'screen-y')
        recognisable_line_arr = self.calculate_line_visibility(fovea_x, fovea_y)
        for line_stim in recognisable_line_arr:
            # actr.add_dm_chunks(line_stim.chunk_name)
            actr.merge_dm_chunks(line_stim.chunk_name)

    def attach_pattern_chunk_into_root_in_goal(self, pattern_chunk_name, goal_chunk_name):
        goal_root_chunk_name = actr.chunk_slot_value(goal_chunk_name, 'chunking-root')
        if goal_root_chunk_name is None:
            goal_root_chunk_name = actr.define_chunks(['isa', 'figure'])[0]

        slot_chunk_name_pair = self.get_chunk_slot_values(goal_root_chunk_name)

        # test code
        print(goal_root_chunk_name)
        print(slot_chunk_name_pair)

        chunk_name_set = set(k[1] for k in slot_chunk_name_pair)
        chunk_type_list = list(actr.chunk_slot_value(el, "LABEL") for el in chunk_name_set)
        arg_chunk_type = actr.chunk_slot_value(pattern_chunk_name, "LABEL")
        if arg_chunk_type in chunk_type_list:
            return
        slot_name_set = list(k for k in slot_chunk_name_pair if k[0].startswith('SLOT'))
        next_empty_slot_idx = len(slot_name_set) + 1
        actr.set_chunk_slot_value(goal_root_chunk_name, 'slot-' + str(next_empty_slot_idx), pattern_chunk_name)
        actr.set_chunk_slot_value(goal_chunk_name, 'chunking-root', goal_root_chunk_name)

    def clear_tmp_imaginal_buffer_chunk(self, chunk_name):
        slot_chunk_name_pair = self.get_chunk_slot_values(chunk_name)
        for slot_value_pair in slot_chunk_name_pair:
            actr.set_chunk_slot_value(chunk_name, slot_value_pair[0], 'nil')

    def identify_patterns_from_line_group_chunk(self, buffer_chunk, pattern_label):
        # imaginal_buffer_content = actr.buffer_chunk('imaginal')[0]
        slot_chunk_name_pair = self.get_chunk_slot_values(buffer_chunk)
        chunk_name_object_dict = self.get_line_object_in_tuple_list(slot_chunk_name_pair)

        # check whether all the target pattern lines are all included in imaginal
        num_line_in_pattern = self.pattern_stroke_num[pattern_label]
        num_line_in_imaginal = 0
        for line in chunk_name_object_dict.values():
            if line.type_tag == pattern_label:
                num_line_in_imaginal += 1
                # print(line.chunk_name, line.type_tag, line.size)
        # print(num_line_in_imaginal, num_line_in_pattern)

        if num_line_in_imaginal == num_line_in_pattern:
            # return 'found'
            # pattern_spatial_info_list = self.get_nearby_patterns_from_visiable_lines(chunk_name_object_dict, pattern_label)
            line_group_chunk_name = self.create_pattern_chunk_with_label(pattern_label)
            # line_group_chunk_name = self.create_patern_chunk_with_label_and_spatial_info(pattern_label, pattern_spatial_info_list)
            # actr.add_dm_chunks(line_group_chunk_name)
            actr.merge_dm_chunks(line_group_chunk_name)
            return line_group_chunk_name
        else:
            return 'not-found'

    def get_nearby_patterns_from_visiable_lines(self, chunk_name_object_dict, tar_pattern_label):
        pattern_dict = {}
        for line_stim in chunk_name_object_dict.values():
            # if line_stim.type_tag != tar_pattern_label:
            # put the line into the nearby pattern dict
            if line_stim.type_tag not in pattern_dict:
                pattern_dict[line_stim.type_tag] = []
            pattern_dict[line_stim.type_tag].append(line_stim)

        # get boundary of each pattern
        pattern_and_boundary_list = []
        tar_pattern_boundary = None
        for key in pattern_dict.keys():
            max_x = -math.inf
            min_x = math.inf
            max_y = -math.inf
            min_y = math.inf
            for line in pattern_dict[key]:
                max_x = max(max_x, max(line.x_s, line.x_e))
                max_y = max(max_y, max(line.y_s, line.y_e))
                min_x = min(min_x, min(line.x_s, line.x_e))
                min_y = min(min_y, min(line.y_s, line.y_e))
            if line.type_tag != tar_pattern_label:
                pattern_and_boundary_list.append((key, (max_x, max_y, min_x, min_y)))
            else:
                tar_pattern_boundary = (max_x, max_y, min_x, min_y)

        # get spatial relations between the target rectangle and other rectangles
        pattern_spatial_info_dict = {}
        for pattern_boundary in pattern_and_boundary_list:
            max_x1, max_y1, min_x1, min_y1 = pattern_boundary[1]
            max_x2, max_y2, min_x2, min_y2 = tar_pattern_boundary

            if max_y1 < min_y2:
                if "above" not in pattern_spatial_info_dict:
                    pattern_spatial_info_dict["above"] = []
                pattern_spatial_info_dict["above"].append((pattern_boundary[0],pattern_boundary[1]))
            elif min_y1 > max_y2:
                if "below" not in pattern_spatial_info_dict:
                    pattern_spatial_info_dict["below"] = []
                pattern_spatial_info_dict["below"].append((pattern_boundary[0],pattern_boundary[1]))
            elif max_x1 < min_x2:
                if "left" not in pattern_spatial_info_dict:
                    pattern_spatial_info_dict["left"] = []
                pattern_spatial_info_dict["left"].append((pattern_boundary[0],pattern_boundary[1]))
            elif min_x1 > max_x2:
                if "right" not in pattern_spatial_info_dict:
                    pattern_spatial_info_dict["right"] = []
                pattern_spatial_info_dict["right"].append((pattern_boundary[0],pattern_boundary[1]))
            elif (min_x1 < max_x2 and max_x1 > min_x2 and min_y1 < max_y2 and max_y1 > min_y2):
                if "overlap" not in pattern_spatial_info_dict:
                    pattern_spatial_info_dict["overlap"] = []
                pattern_spatial_info_dict["overlap"].append((pattern_boundary[0],pattern_boundary[1]))
            else:
                print(pattern_boundary[0])

        pattern_list = []
        for key in pattern_spatial_info_dict.keys():
            value = pattern_spatial_info_dict[key]
            if value.__len__() > 1:
                min_distance = math.inf
                for pattern_boundary in value:
                    max_x1, max_y1, min_x1, min_y1 = tar_pattern_boundary
                    max_x2, max_y2, min_x2, min_y2 = pattern_boundary[1]
                    center_x1 = (max_x1 + min_x1) / 2
                    center_y1 = (max_y1 + min_y1) / 2
                    center_x2 = (max_x2 + min_x2) / 2
                    center_y2 = (max_y2 + min_y2) / 2
                    distance = math.sqrt((center_x1 - center_x2) ** 2 + (center_y1 - center_y2) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                        closest_pattern = pattern_boundary
                pattern_list.append((key,closest_pattern[0]))
            else:
                pattern_list.append((key,value[0][0]))

        return pattern_list

    def identify_patterns_given_current_location(self, buffer_chunk, visual_location):
        screen_x = actr.chunk_slot_value(visual_location, 'screen-x')
        screen_y = actr.chunk_slot_value(visual_location, 'screen-y')
        tar_line_stim = None
        # if self.current_trial_idx == 3:
        #     print('test')
        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                tar_line_stim = line_stim
                break
        line_group_chunk_name = self.identify_patterns_from_line_group_chunk(buffer_chunk, tar_line_stim.type_tag)
        return line_group_chunk_name

    # def identify_pattern_then_save_chunk_in_dm(self, buffer_chunk, visual_location):
    #     chunk_name = self.identify_patterns_given_current_location(buffer_chunk, visual_location)


    def get_furthest_pattern_line_location(self, buffer_chunk, visual_location):

        screen_x = actr.chunk_slot_value(visual_location, 'screen-x')
        screen_y = actr.chunk_slot_value(visual_location, 'screen-y')
        tar_line_stim = None

        print(visual_location, screen_x, screen_y, "get_furthest_pattern_line_location")

        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                tar_line_stim = line_stim
                break

        pattern_line_full_set = set()
        for line_stim in self.line_strokes:
            if line_stim.type_tag == tar_line_stim.type_tag:
                pattern_line_full_set.add(line_stim.chunk_name)

        slot_chunk_name_pair = self.get_chunk_slot_values(buffer_chunk)
        chunk_name_object_dict = self.get_line_object_in_tuple_list(slot_chunk_name_pair)

        pattern_line_not_in_imaginal = pattern_line_full_set - set(chunk_name_object_dict.keys())
        unseen_line_chun_name = random.choice(list(pattern_line_not_in_imaginal))
        unseen_line_stim = self.line_stroke_dict[unseen_line_chun_name]

        # if the pattern is not fully recognisable with all the visible line explored, move attention to the unseen line directly
        if self.pre_tar_screen_x == screen_x and self.pre_tar_screen_y == screen_y:
            return self.create_screen_location(unseen_line_stim.screen_x, unseen_line_stim.screen_y)

        tar_screen_x = unseen_line_stim.screen_x
        tar_screen_y = unseen_line_stim.screen_y
        mim_distance = math.inf
        for line in chunk_name_object_dict.values():
            if line.type_tag == tar_line_stim.type_tag:
                tmp_distance = math.sqrt((line.screen_x - unseen_line_stim.screen_x) ** 2 + (line.screen_y - unseen_line_stim.screen_y) ** 2)
                if tmp_distance < mim_distance:
                    mim_distance = tmp_distance
                    tar_screen_x = line.screen_x
                    tar_screen_y = line.screen_y

        self.pre_tar_screen_x = tar_screen_x
        self.pre_tar_screen_y = tar_screen_y

        print(tar_screen_x, tar_screen_y)
        next_visual_location = self.create_screen_location(tar_screen_x, tar_screen_y)
        return next_visual_location

    def get_furthest_pattern_line_chunk_name(self, buffer_chunk, visual_location):
        tar_line_stim = self.get_furthest_pattern_line_chunk_obj(buffer_chunk, visual_location)
        return tar_line_stim.chunk_name

    def get_furthest_pattern_line_chunk_obj(self, buffer_chunk, visual_location):
        screen_x = actr.chunk_slot_value(visual_location, 'screen-x')
        screen_y = actr.chunk_slot_value(visual_location, 'screen-y')
        current_line_stim = None

        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                current_line_stim = line_stim
                break

        pattern_line_full_set = set()
        for line_stim in self.line_strokes:
            if line_stim.type_tag == current_line_stim.type_tag:
                pattern_line_full_set.add(line_stim.chunk_name)

        slot_chunk_name_pair = self.get_chunk_slot_values(buffer_chunk)
        chunk_name_object_dict = self.get_line_object_in_tuple_list(slot_chunk_name_pair)

        pattern_line_not_in_imaginal = pattern_line_full_set - set(chunk_name_object_dict.keys())
        unseen_line_chun_name = random.choice(list(pattern_line_not_in_imaginal))
        unseen_line_stim = self.line_stroke_dict[unseen_line_chun_name]

        # if the pattern is not fully recognisable with all the visible line explored, move attention to the unseen line directly
        if self.pre_tar_screen_x == screen_x and self.pre_tar_screen_y == screen_y:
            return unseen_line_stim

        tar_line_stim = None
        mim_distance = math.inf
        for line in chunk_name_object_dict.values():
            if line.type_tag == current_line_stim.type_tag:
                tmp_distance = math.sqrt(
                    (line.screen_x - unseen_line_stim.screen_x) ** 2 + (line.screen_y - unseen_line_stim.screen_y) ** 2)
                if tmp_distance < mim_distance:
                    mim_distance = tmp_distance
                    tar_line_stim = line

        if tar_line_stim is None:
            return unseen_line_stim

        self.pre_tar_screen_x = tar_line_stim.screen_x
        self.pre_tar_screen_y = tar_line_stim.screen_y
        return tar_line_stim

    def get_next_pattern_line_location(self, buffer_chunk, visual_location):
        screen_x = actr.chunk_slot_value(visual_location, 'screen-x')
        screen_y = actr.chunk_slot_value(visual_location, 'screen-y')
        tar_line_stim = None

        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                tar_line_stim = line_stim
                break

        slot_chunk_name_pair = self.get_chunk_slot_values(buffer_chunk)
        line_stim_in_buffer = list(self.get_line_object_in_tuple_list(slot_chunk_name_pair).values())
        next_pattern_line_stim_list = list(el for el in line_stim_in_buffer if el.type_tag == tar_line_stim.type_tag and not el.reproduced)
        if len(next_pattern_line_stim_list) == 0:
            return 'not-found'
        next_pattern_line_stim = next_pattern_line_stim_list[0]
        next_visual_location = self.create_screen_location(next_pattern_line_stim.screen_x, next_pattern_line_stim.screen_y)
        return next_visual_location

    def get_current_fixated_line_chunk_name(self, visual_location):
        screen_x = actr.chunk_slot_value(visual_location, 'screen-x')
        screen_y = actr.chunk_slot_value(visual_location, 'screen-y')

        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                return line_stim.chunk_name

    def get_line_end_location(self, line_chunk_name, end_point_tag):
        if line_chunk_name not in self.line_stroke_dict.keys():
            line_chunk_name = line_chunk_name[:line_chunk_name.rfind('-')]
        line_stim = self.line_stroke_dict[line_chunk_name]
        if end_point_tag == 'start':
            return self.create_screen_location(line_stim.x_s, line_stim.y_s)
        elif end_point_tag == 'end':
            return self.create_screen_location(line_stim.x_e, line_stim.y_e)
        elif end_point_tag == 'mid':
            return self.create_screen_location(line_stim.screen_x, line_stim.screen_y)

    def get_chunk_slot_values(self, tar_chunk_name):
        chunk_content_list = []
        filled_slot_name = actr.chunk_filled_slots_list(tar_chunk_name)

        if filled_slot_name is None:
            return chunk_content_list

        filled_slot_name = list(reversed(filled_slot_name))
        for slot_name in filled_slot_name:
            slot_value = actr.chunk_slot_value(tar_chunk_name,slot_name)
            chunk_content_list.append((slot_name, slot_value))
        return chunk_content_list

    def get_line_object_in_tuple_list(self, chunk_content_list):
        line_stim_dict = dict((el[1], None) for el in chunk_content_list)
        for line_stim in self.line_strokes:
            if line_stim.chunk_name in line_stim_dict:
                line_stim_dict[line_stim.chunk_name] = line_stim
        return line_stim_dict

    def put_recognisable_line_into_dm(self, visual_location):
        fovea_x = actr.chunk_slot_value(visual_location, 'screen-x')
        fovea_y = actr.chunk_slot_value(visual_location, 'screen-y')

        # find which line is recognisable
        recognisable_line_arr = self.calculate_line_visibility(fovea_x, fovea_y)

        if ENABLE_BASE_LEVEL_DIFFERENCES:
            # calculate reference count based on eccentricity
            proportion_dict = {}
            total_prop = 0
            for line_stim_name in self.line_chunk_names:
                x_coord = actr.chunk_slot_value(line_stim_name, 'screen-x')
                y_coord = actr.chunk_slot_value(line_stim_name, 'screen-y')
                distance_in_angle = math.sqrt(
                    (x_coord - fovea_x) ** 2 + (y_coord - fovea_y) ** 2) / PIXELS_PER_VIEWING_ANGLE
                # calculate the Acuity proportion based on y =  e ^ -(0.13 * x), x is the distance in angle
                cur_prop = math.exp(-0.13 * distance_in_angle)
                total_prop += cur_prop
                proportion_dict[line_stim_name] = cur_prop

        for line_stim in recognisable_line_arr:
            # actr.add_dm_chunks(line_stim.chunk_name)
            actr.merge_dm_chunks(line_stim.chunk_name)
            if ENABLE_BASE_LEVEL_DIFFERENCES:
                cur_reference_count = actr.sdp(line_stim.chunk_name, ':reference-count')[0][0]
                actr.set_base_level(line_stim.chunk_name, cur_reference_count + (
                        self.total_reference_count * (proportion_dict[line_stim.chunk_name] / total_prop)))

    def add_line_locations_into_dm(self, current_location):
        visicon_str = actr.printed_visicon()
        # visicon_content_arr = list(filter(lambda x: x.startswith("VISUAL-LOCATION"), visicon_str.split('\n')))
        visicon_content_arr = list(
            filter(lambda x: ("LINE" in x) & x.startswith("VISUAL-LOCATION"), visicon_str.split('\n')))
        self.line_num = len(visicon_content_arr)

        # create disc chunks and store the names of those chunks
        self.line_chunk_names = []
        self.line_strokes = []
        for loc_str in visicon_content_arr:
            location_str = loc_str[loc_str.index('(') + 1:loc_str.index(')')].strip()
            coord_arr = location_str.split()
            coord_x = int(coord_arr[0])
            coord_y = int(coord_arr[1])
            line_number_str = loc_str.split()[0]
            line_number_str = line_number_str[line_number_str.index('N') + 1:]
            line_label_str = 'line-label-' + line_number_str

            line_coords = loc_str.split()[-4:]
            line_color = loc_str[loc_str.index(' "') + 2:loc_str.index('" ')].strip()
            actr.define_chunks(line_label_str)
            tmp_chunk_name = actr.define_chunks(
                ['isa', 'line-stimulus', 'color', line_color, 'label', line_label_str, 'screen-x', coord_x, 'screen-y',
                 coord_y, 'x-s', line_coords[3], 'y-s', line_coords[2], 'x-e', line_coords[1], 'y-e', line_coords[0]])[
                0]
            tmp_line_obj = line_stroke.LineStroke(coord_x, coord_y, int(line_coords[3]), int(line_coords[2]),
                                                  int(line_coords[1]), int(line_coords[0]))
            tmp_line_obj.label_slot_value = line_label_str
            self.line_strokes.append(tmp_line_obj)
            # print(tmp_chunk_name)
            self.line_chunk_names.append(tmp_chunk_name)
            # actr.add_dm_chunks(tmp_chunk_name)
            actr.merge_dm_chunks(tmp_chunk_name)

            # # set initial reference count to 0
            actr.set_base_level(tmp_chunk_name, 0)

        self.calculate_reference_count_base_on_location(current_location)

    def calculate_reference_count_base_on_location(self, current_location):
        fovea_x = actr.chunk_slot_value(current_location, 'screen-x')
        fovea_y = actr.chunk_slot_value(current_location, 'screen-y')

        # Equation: receptive field size = 0.0615 * eccentricity
        # find which line is recognisable
        # recognisable_line = []
        # for line_stim in self.line_strokes:
        #     distance_to_fovea = math.sqrt((line_stim.screen_x - fovea_x) ** 2 + (line_stim.screen_y - fovea_y) ** 2) / PIXELS_PER_VIEWING_ANGLE
        #     line_len_in_angle = math.sqrt((line_stim.x_s - line_stim.x_e) ** 2 + (line_stim.y_s - line_stim.y_e) ** 2) / PIXELS_PER_VIEWING_ANGLE
        #     receptive_field_size = 0.0615 * distance_to_fovea
        #     if line_len_in_angle > receptive_field_size:
        #         recognisable_line.append(line_stim)
        # print(recognisable_line)
        self.get_shape_availability(current_location)

        # calculate shares based on the distance to the fovea location
        proportion_dict = {}
        total_prop = 0
        for line_stim_name in self.line_chunk_names:
            x_coord = actr.chunk_slot_value(line_stim_name, 'screen-x')
            y_coord = actr.chunk_slot_value(line_stim_name, 'screen-y')
            distance_in_angle = math.sqrt(
                (x_coord - fovea_x) ** 2 + (y_coord - fovea_y) ** 2) / PIXELS_PER_VIEWING_ANGLE

            # calculate the Acuity proportion based on y =  e ^ -(0.13 * x), x is the distance in angle
            cur_prop = math.exp(-0.13 * distance_in_angle)

            total_prop += cur_prop
            proportion_dict[line_stim_name] = cur_prop

        for line_stim_name in self.line_chunk_names:
            cur_reference_count = actr.sdp(line_stim_name, ':reference-count')[0][0]
            # cur_reference_count = 0

            # set based on fixed total
            actr.set_base_level(line_stim_name, cur_reference_count + (
                    self.total_reference_count * (proportion_dict[line_stim_name] / total_prop)))

    def get_shape_availability(self, current_location):
        fovea_x = actr.chunk_slot_value(current_location, 'screen-x')
        fovea_y = actr.chunk_slot_value(current_location, 'screen-y')

        # Equation: threshold = 0.3 (e ** 2) + 0.1 e + 0.1
        #           X ~ N (0.7 * s)
        # find which line is recognisable

        pixel_per_viewing_angle = self.calculate_pixel_per_viewing_angle()
        recognisable_line = []
        for line_stim in self.line_strokes:
            eccentricity = math.sqrt(
                (line_stim.screen_x - fovea_x) ** 2 + (line_stim.screen_y - fovea_y) ** 2) / pixel_per_viewing_angle
            threshold_shape = 0.3 * (eccentricity ** 2) + 0.1 * eccentricity + 0.1
            gaussian_noise = random.gauss(0, 0.7 * line_stim.size)
            if line_stim.size > threshold_shape + gaussian_noise:
                line_stim.eccentricity = eccentricity
                recognisable_line.append(line_stim)

        # self.test_show_visiable_lines(recognisable_line)
        self.create_line_group_chunk(recognisable_line)
        # line_len_in_angle = math.sqrt(
        #     (line_stim.x_s - line_stim.x_e) ** 2 + (line_stim.y_s - line_stim.y_e) ** 2) / pixel_per_viewing_angle
        # receptive_field_size = 0.0615 * distance_to_fovea
        # if line_len_in_angle > receptive_field_size:
        #     recognisable_line.append(line_stim)

    def create_line_group_chunk(self, recognisable_line):
        self.test_show_visiable_lines(recognisable_line)
        recognisable_line = list(filter(lambda x: x not in self.line_in_groups, recognisable_line))
        if len(recognisable_line) > MAX_LINE_NUM_PER_GROUP:
            recognisable_line = sorted(recognisable_line, key=lambda line: line.eccentricity)
            recognisable_line = recognisable_line[0:MAX_LINE_NUM_PER_GROUP]
        line_group_label_str = 'group-' + str(self.line_group_label_idx)
        chunk_param_list = ['isa', 'line-group', 'label', line_group_label_str]
        actr.define_chunks(line_group_label_str)
        self.line_group_label_idx += 1
        for idx, line in enumerate(recognisable_line):
            chunk_param_list.append('x-s-' + str(idx + 1))
            chunk_param_list.append(str(line.x_s))
            chunk_param_list.append('y-s-' + str(idx + 1))
            chunk_param_list.append(str(line.y_s))
            chunk_param_list.append('x-e-' + str(idx + 1))
            chunk_param_list.append(str(line.x_e))
            chunk_param_list.append('y-e-' + str(idx + 1))
            chunk_param_list.append(str(line.y_e))
            chunk_param_list.append('line-label-' + str(idx + 1))
            chunk_param_list.append(str(line.label_slot_value))

            # define new similarity between line_label and line_group_label for partial matching
            actr.set_similarities([str(line.label_slot_value), line_group_label_str, 0],
                                  [line_group_label_str, str(line.label_slot_value), 0])

        # create line group chunk
        tmp_chunk_name = actr.define_chunks(chunk_param_list)
        # actr.add_dm_chunks(tmp_chunk_name)
        actr.merge_dm_chunks(tmp_chunk_name)
        self.line_in_groups = self.line_in_groups + recognisable_line

        return tmp_chunk_name

    def calculate_pixel_per_viewing_angle(self):
        len_in_inch = math.tan(math.radians(0.5)) * VIEWING_DISTANCE_INCH * 2
        self.pixels_per_angle = round(len_in_inch * PIXELS_PER_INCH)
        return self.pixels_per_angle
        # len_in_inch = self.pixels_per_angle / PIXELS_PER_INCH
        # math.tan(0.5) = len_in_inch/ 2 / VIEWING_DISTANCE_INCH

    def get_center_x_of_figure(self):
        return np.median(np.array(self.stim_xs + self.stim_xe))

    def get_center_y_of_figure(self):
        return np.median(np.array(self.stim_ys + self.stim_ye))

    def put_body_group_into_visal_buffer(self):
        self.create_pattern_chunk_with_label('body')

    def put_box_group_into_visal_buffer(self):
        self.create_pattern_chunk_with_label('box')
        # chunk_param_list = ['isa', 'line-group', 'label', 'group-box']
        # tar_line_idx = []
        # for idx, tag in enumerate(LINE_TAG):
        #     if tag == 'box':
        #         tar_line_idx.append(idx)
        #
        # for idx, line_idx in enumerate(tar_line_idx):
        #     chunk_param_list.append('x-s-' + str(idx + 1))
        #     chunk_param_list.append(str(self.stim_xs[line_idx]))
        #     chunk_param_list.append('y-s-' + str(idx + 1))
        #     chunk_param_list.append(str(self.stim_ys[line_idx]))
        #     chunk_param_list.append('x-e-' + str(idx + 1))
        #     chunk_param_list.append(str(self.stim_xe[line_idx]))
        #     chunk_param_list.append('y-e-' + str(idx + 1))
        #     chunk_param_list.append(str(self.stim_ye[line_idx]))
        #     actr.set_similarities([str(self.line_strokes[line_idx].label_slot_value), 'group-box', 0],
        #                           ['group-box', str(self.line_strokes[line_idx].label_slot_value), 0])
        # tmp_chunk_name = actr.define_chunks(chunk_param_list)[0]
        # actr.set_buffer_chunk('visual', tmp_chunk_name)

    def create_pattern_chunk_with_label(self, pattern_label):
        chunk_param_list = ['isa', 'line-group', 'type', 'group-' + pattern_label, 'label', pattern_label, 'chunk-type-tag', 'line-group']

        max_x = -math.inf
        min_x = math.inf
        max_y = -math.inf
        min_y = math.inf
        tar_line_chunk_name_arr = []
        for line in self.line_strokes:
            if line.type_tag == pattern_label:
                tar_line_chunk_name_arr.append(line.chunk_name)
                max_x = max(max_x, max(line.x_s, line.x_e))
                max_y = max(max_y, max(line.y_s, line.y_e))
                min_x = min(min_x, min(line.x_s, line.x_e))
                min_y = min(min_y, min(line.y_s, line.y_e))

        chunk_param_list.append('screen-x')
        chunk_param_list.append(str((max_x + min_x) / 2))
        chunk_param_list.append('screen-y')
        chunk_param_list.append(str((max_y + min_y) / 2))

        for idx, chunk_name in enumerate(tar_line_chunk_name_arr):
            chunk_param_list.append('line' + str(idx + 1))
            chunk_param_list.append(chunk_name)
            # actr.add_dm_chunks(chunk_name)
            actr.merge_dm_chunks(chunk_name)

        tmp_chunk_name = actr.define_chunks(chunk_param_list)[0]
        # actr.set_buffer_chunk('visual', tmp_chunk_name)
        # if tmp_chunk_name not in self.pattern_chunk_name_set:
        #     self.pattern_chunk_name_set.add(tmp_chunk_name)

        return tmp_chunk_name

    def create_patern_chunk_with_label_and_spatial_info(self, pattern_label, nearby_patterns):
        chunk_param_list = ['isa', 'line-group', 'type', 'group-' + pattern_label, 'label', pattern_label,
                            'chunk-type-tag', 'line-group']

        max_x = -math.inf
        min_x = math.inf
        max_y = -math.inf
        min_y = math.inf
        tar_line_chunk_name_arr = []
        for line in self.line_strokes:
            if line.type_tag == pattern_label:
                tar_line_chunk_name_arr.append(line.chunk_name)
                max_x = max(max_x, max(line.x_s, line.x_e))
                max_y = max(max_y, max(line.y_s, line.y_e))
                min_x = min(min_x, min(line.x_s, line.x_e))
                min_y = min(min_y, min(line.y_s, line.y_e))

        chunk_param_list.append('screen-x')
        chunk_param_list.append(str((max_x + min_x) / 2))
        chunk_param_list.append('screen-y')
        chunk_param_list.append(str((max_y + min_y) / 2))

        for idx, chunk_name in enumerate(tar_line_chunk_name_arr):
            chunk_param_list.append('line' + str(idx + 1))
            chunk_param_list.append(chunk_name)
            actr.merge_dm_chunks(chunk_name)

        tmp_chunk_name = actr.define_chunks(chunk_param_list)[0]

        return tmp_chunk_name

    def get_line_location(self, pattern_label, location_label):
        tar_lines_arr = []
        for line in self.line_strokes:
            if line.type_tag == pattern_label:
                tar_lines_arr.append(line)

        if location_label == 'left':
            tar_lines_arr.sort(key=lambda x: x.screen_x)
        elif location_label == 'right':
            tar_lines_arr.sort(key=lambda x: x.screen_x, reverse=True)
        elif location_label == 'top':
            tar_lines_arr.sort(key=lambda x: x.screen_y)
        elif location_label == 'bottom':
            tar_lines_arr.sort(key=lambda x: x.screen_y, reverse=True)

        return self.create_screen_location(tar_lines_arr[0].screen_x, tar_lines_arr[0].screen_y)

    def create_screen_location(self, x, y):
        # print(pattern_chunk)
        return actr.define_chunks(['isa', 'visual-location', 'screen-x', x, 'screen-y', y, 'distance',
                                   VIEWING_DISTANCE_INCH * PIXELS_PER_INCH])[0]

    def get_line_slot_base_on_imaginal(self):
        chunk_name = actr.buffer_chunk('imaginal')[0]
        next_slot_name = 'line' + str(self.current_line_slot_idx + 1)
        if actr.chunk_slot_value(chunk_name, next_slot_name) is not None:
            self.current_line_slot_idx += 1
            # return next_slot_name
        else:
            self.current_line_slot_idx = 0
        return next_slot_name

    def get_line_slot_from_line_group(self, line_group_chunk):
        if line_group_chunk != self.current_ling_group_name:
            self.current_line_slot_idx = 1
            self.current_ling_group_name = line_group_chunk
        next_slot_name = 'line' + str(self.current_line_slot_idx)

        if actr.chunk_slot_value(line_group_chunk, next_slot_name) is not None:
            self.current_line_slot_idx += 1
            return next_slot_name
        else:
            self.current_line_slot_idx = 1
            return 'not-found'

    def draw_line_for_copying(self, y_shifting):

        chunk_name = actr.buffer_chunk('retrieval')[0]
        xs = int(actr.chunk_slot_value(chunk_name, 'x-s'))
        ys = int(actr.chunk_slot_value(chunk_name, 'y-s'))
        xe = int(actr.chunk_slot_value(chunk_name, 'x-e'))
        ye = int(actr.chunk_slot_value(chunk_name, 'y-e'))
        actr.add_line_to_exp_window(self.stim_window, [xs, ys + y_shifting], [xe, ye + y_shifting], ["white"])

    def add_responded_line_to_response_panel(self, line_chunk_name):
        xs = int(actr.chunk_slot_value(line_chunk_name, 'x-s'))
        ys = int(actr.chunk_slot_value(line_chunk_name, 'y-s'))
        xe = int(actr.chunk_slot_value(line_chunk_name, 'x-e'))
        ye = int(actr.chunk_slot_value(line_chunk_name, 'y-e'))
        actr.add_line_to_exp_window(self.resp_window, [xs, ys], [xe, ye], ["black"])

        screen_x = actr.chunk_slot_value(line_chunk_name, 'screen-x')
        screen_y = actr.chunk_slot_value(line_chunk_name, 'screen-y')

        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                line_stim.reproduced = True
                break

        # self.line_stroke_dict[line_chunk_name].is_responded = True

    def get_tar_line_stim_chunk_name(self, visual_location):
        screen_x = actr.chunk_slot_value(visual_location, 'screen-x')
        screen_y = actr.chunk_slot_value(visual_location, 'screen-y')
        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                return line_stim.chunk_name
        return None


    def record_drawing_time(self, timing_type):
        if timing_type == 'start':
            self.drawing_start_time_list.append(actr.get_time(True))
        elif timing_type == 'end':
            self.drawing_end_time_list.append(actr.get_time(True))

    def record_response_line_type(self, line_chunk_name):
        self.drawing_line_type_list.append(actr.chunk_slot_value(line_chunk_name, 'label'))

        # code for debugging
        print('line type: ', actr.chunk_slot_value(line_chunk_name, 'label'))
        print('screen-x: ', actr.chunk_slot_value(line_chunk_name, 'screen-x'))
        print('screen-x: ', actr.chunk_slot_value(line_chunk_name, 'screen-y'))

    def check_all_line_is_repreduced(self):
        num_unresponded_line = list(el for el in self.line_strokes if el.reproduced == False)
        print('num_unresponded_line: ', len(num_unresponded_line))
        if len(num_unresponded_line) > 0:
            return 'not-finish'
        else:
            return 'finish'

    def get_location_of_unreproduced_line(self):
        line_chunk_name = 'not-found'
        for line_stim in self.line_strokes:
            if line_stim.reproduced == False:
                line_chunk_name = line_stim.chunk_name
                break
        return line_chunk_name

    def get_next_pattern_line_chunk_name_for_copying(self, visual_location):
        # pre_pattern_name = self.drawing_line_type_list[-1]
        # pre_pattern_name = pre_pattern_name.lower()

        screen_x = actr.chunk_slot_value(visual_location, 'screen-x')
        screen_y = actr.chunk_slot_value(visual_location, 'screen-y')
        cur_line_stim = None
        for line_stim in self.line_strokes:
            if line_stim.screen_x == screen_x and line_stim.screen_y == screen_y:
                cur_line_stim = line_stim
                break

        min_distance = math.inf
        tar_line_stim = None
        for line_stim in self.line_strokes:
            tmp_distance = math.sqrt((line_stim.screen_x - cur_line_stim.screen_x) ** 2 + (
                        line_stim.screen_y - cur_line_stim.screen_y) ** 2)
            if tmp_distance < min_distance and line_stim.reproduced == False and line_stim.chunk_name != cur_line_stim.chunk_name:
                min_distance = tmp_distance
                tar_line_stim = line_stim

        if tar_line_stim is None:
            return 'not-found'

        return tar_line_stim.chunk_name

    def get_line_end_2_coord(self, line_chunk_name, x_or_y):
        # x-e ==> end-2x
        xe = int(actr.chunk_slot_value(line_chunk_name, 'x-e')) + self.copy_window_offset
        ye = int(actr.chunk_slot_value(line_chunk_name, 'y-e')) + self.copy_window_offset

        print(xe, ye)
        if x_or_y.lower() == 'x':
            return xe
        elif x_or_y.lower() == 'y':
            return ye
        return None

    def update_visual_location_for_copying(self, visual_location):
        screen_x = int(actr.chunk_slot_value(visual_location, 'screen-x')) - self.copy_window_offset
        screen_y = int(actr.chunk_slot_value(visual_location, 'screen-y')) - self.copy_window_offset

        # actr.set_chunk_slot_value(visual_location, 'screen-x', screen_x)
        # actr.set_chunk_slot_value(visual_location, 'screen-y', screen_y)
        return self.create_screen_location(screen_x, screen_y)

    def check_whether_pattern_is_reproduce_finished(self, pattern_chunk_name):
        pattern_type_tag = actr.chunk_slot_value(pattern_chunk_name, 'label').lower()
        un_reproduced_line = list(el for el in self.line_strokes if el.reproduced == False and el.type_tag == pattern_type_tag)
        if len(un_reproduced_line) == 0:
            return 'not-found'
        else:
            # return self.create_screen_location(un_reproduced_line[0].screen_x + self.copy_window_offset,
            #                                    un_reproduced_line[0].screen_y + self.copy_window_offset)
            return un_reproduced_line[0].chunk_name



    # ==============================================================================================================
    # test code
    # ==============================================================================================================

    def break_point_for_test(self, input = None):
        print('test:', input)

    def test_show_visiable_lines(self, recognisable_line):
        # for line_id_info in self.test_line_id:
        #     actr.remove_items_from_exp_window(None, line_id_info[1])
        self.test_line_id = []
        y_shift = 500
        for line in recognisable_line:
            line_id_info = actr.add_line_to_exp_window(self.stim_window, [line.x_s, y_shift + line.y_s],
                                                       [line.x_e, y_shift + line.y_e], ["white"])
            self.test_line_id.append(line_id_info)

    def test_show_symetric_line(self, line_stim_list):

        for line_stim in self.line_strokes:
            plt.plot(np.array([line_stim.x_s, line_stim.x_e]), -np.array([line_stim.y_s, line_stim.y_e]), '--b')
        for line_stim in line_stim_list:
            plt.plot(np.array([line_stim.x_s, line_stim.x_e]), -np.array([line_stim.y_s, line_stim.y_e]), 'r')
        plt.ylim(-1000, 0)
        plt.xlim(0, 1600)
        plt.show()

    def test_show_all_symetric_line_of_each_line(self):
        
        line_list_pair = []
        for line_chunk_name, symetric_line_list in self.line_symmetry_dict.items():
            for line_stim in self.line_strokes:
                if line_stim.chunk_name == line_chunk_name and line_stim.type_tag == 'tail':
                    line_list_pair.append((line_stim, symetric_line_list))

        for tar_line, symetric_line_list in line_list_pair:
            if len(symetric_line_list) == 0:
                continue
            for line_stim in self.line_strokes:
                plt.plot(np.array([line_stim.x_s, line_stim.x_e]), -np.array([line_stim.y_s, line_stim.y_e]), '--b')
            plt.plot(np.array([tar_line.x_s, tar_line.x_e]), -np.array([tar_line.y_s, tar_line.y_e]), 'g')
            for line_stim in symetric_line_list:
                plt.plot(np.array([line_stim.x_s, line_stim.x_e]), -np.array([line_stim.y_s, line_stim.y_e]), 'r')
            plt.ylim(-1000, 0)
            plt.xlim(0, 1600)
            plt.show()


    def test_show_all_linked_line_of_each_line(self):
        line_list_pair = []
        for line_chunk_name, adjacency_line_list in self.line_connection_list.items():
            for line_stim in self.line_strokes:
                if line_stim.chunk_name == line_chunk_name:
                    line_list_pair.append((line_stim, adjacency_line_list))

        for tar_line, adjacency_line_list in line_list_pair:
            if len(adjacency_line_list) == 0:
                continue
            for line_stim in self.line_strokes:
                plt.plot(np.array([line_stim.x_s, line_stim.x_e]), -np.array([line_stim.y_s, line_stim.y_e]), '--b')
            plt.plot(np.array([tar_line.x_s, tar_line.x_e]), -np.array([tar_line.y_s, tar_line.y_e]), 'g')
            for line_stim in adjacency_line_list:
                plt.plot(np.array([line_stim.x_s, line_stim.x_e]), -np.array([line_stim.y_s, line_stim.y_e]), 'r')
            plt.ylim(-1000, 0)
            plt.xlim(0, 1600)
            plt.show()

    def test_find_tar_lines_using_tag(self):
        tar_lines = []
        for line_stim in self.line_strokes:
            if line_stim.type_tag == 'tail':
                tar_lines.append(line_stim)
                print(math.degrees(math.atan(line_stim.slope)), (line_stim.x_e - line_stim.x_s) , (line_stim.y_e - line_stim.y_s))
        print(tar_lines)

        horizontal_lines = []
        for line_stim in tar_lines:
            if line_stim.horizontal:
                horizontal_lines.append(line_stim)

        tar_lines_idx = np.array(LINE_TAG) == 'tail'
        xs_arr = np.array(STIMLUS_XS)[tar_lines_idx]
        ys_arr = np.array(STIMLUS_YS)[tar_lines_idx]
        xe_arr = np.array(STIMLUS_XE)[tar_lines_idx]
        ye_arr = np.array(STIMLUS_YE)[tar_lines_idx]

        x_diff = abs(xe_arr - xs_arr)
        y_diff = abs(ye_arr - ys_arr)
        for i in range(len(x_diff)):
            for line_stim in horizontal_lines:
                if x_diff[i] == abs(line_stim.x_e - line_stim.x_s) and y_diff[i] == abs(line_stim.y_e - line_stim.y_s):
                    print(xs_arr[i], ys_arr[i], xe_arr[i], ye_arr[i])
                    print(math.degrees(math.atan(line_stim.slope)), (line_stim.x_e - line_stim.x_s) , (line_stim.y_e - line_stim.y_s))
                    print(x_diff[i], y_diff[i])




def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def point_on_segment(point, segment):
    x, y = point
    x1, y1 = segment[0]
    x2, y2 = segment[1]

    # Check if the point is within the bounding box of the line segment
    if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        # Calculate the cross product
        cross_product = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)

        # Check if the cross product is zero, indicating collinearity
        if abs(cross_product - 0) < 0.0001:
            return True

    return False

def test_size(height, width):
    height_inch = height / PIXELS_PER_INCH
    width_inch = width / PIXELS_PER_INCH
    height_in_angle = math.degrees(2 * math.atan(height_inch / 2 / VIEWING_DISTANCE_INCH))
    width_in_angle = math.degrees(2 * math.atan(width_inch / 2 / VIEWING_DISTANCE_INCH))
    print(height_in_angle * width_in_angle)


def main():
    # test_size(327,6)
    # actr.load_act_r_model("ACT-R:workspace;test.lisp")
    actr.load_act_r_model("ACT-R:workspace;fixed_pattern_model.lisp")
    # actr.load_act_r_code("ACT-R:workspace;fixed_pattern_trace_by_memory_model.lisp")
    test = FigureDrawingMdeol()
    # test.run_experiment(True, TOTAL_REFERENCE_NUM)
    test.run_experiment(False, TOTAL_REFERENCE_NUM)

    data = test.experiment_result
    # print(data)
    #
    # import generate_figure_for_data
    # generate_figure_for_data.plot_sequence_matrix(generate_figure_for_data.pad_sequence(data))

    # save data into pickle file
    with open('experiment_data_fixed.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)






if __name__ == '__main__':
    main()
