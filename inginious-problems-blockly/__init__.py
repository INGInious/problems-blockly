# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

import os
import web
import json

from inginious.common.tasks_problems import Problem
from inginious.frontend.task_problems import DisplayableProblem

__version__ = "0.1.dev0"

PATH_TO_PLUGIN = os.path.abspath(os.path.dirname(__file__))


class StaticMockPage(object):
    # TODO: Replace by shared static middleware and let webserver serve the files
    def GET(self, path):
        if not os.path.abspath(PATH_TO_PLUGIN) in os.path.abspath(os.path.join(PATH_TO_PLUGIN, path)):
            raise web.notfound()

        try:
            with open(os.path.join(PATH_TO_PLUGIN, "static", path), 'rb') as file:
                return file.read()
        except:
            raise web.notfound()

    def POST(self, path):
        return self.GET(path)


class BlocklyProblem(Problem):
    """
    Blockly problem
    """
    def __init__(self, task, problemid, content, translations=None):
        super(BlocklyProblem, self).__init__(task, problemid, content, translations)
        self._toolbox = content.get("toolbox", "<xml></xml>")
        self._workspace = content.get("workspace", "")
        self._options = content.get("options", [])
        self._files = content.get("files", [])
        self._blocks_files = content.get("blocks_files", [])

    @classmethod
    def get_type(self):
        return "blockly"

    def input_type(self):
        """ Indicates if problem input type """
        return str

    @classmethod
    def parse_problem(cls, problem_content):
        # Blockly related checks

        if "options" in problem_content:
            blockly_options = ['collapse', 'comments', 'disable', 'trashcan', 'horizontalLayout', 'css',
                               'oneBasedIndex', 'readOnly', 'rtl',  'scrollbars', 'sounds']
            problem_options = problem_content['options']
            for option in blockly_options:
                if option in problem_options:
                    problem_options[option] = True

        if "visual" in problem_options:
            visual_options = problem_options["visual"]
            visual_options["position"] = visual_options["position"] if "position" in visual_options else "right"

        if "grid" in problem_options:
            grid_options = problem_options["grid"]
            grid_options["snap"] = True if "snap" in grid_options else False
            grid_options["length"] = int(grid_options["length"]) if "length" in grid_options else 3
            grid_options["colour"] = grid_options["colour"] if "colour" in grid_options else "#ccc"
            grid_options["spacing"] = int(grid_options["spacing"]) if "spacing" in grid_options else 20

        if "zoom" in problem_options:
            zoom_options = problem_options["zoom"]
            zoom_options["scaleSpeed"] = float(zoom_options["scaleSpeed"]) if "scaleSpeed" in zoom_options else 1.2
            zoom_options["controls"] = True if "controls" in zoom_options else False
            zoom_options["minScale"] = float(zoom_options["minScale"]) if "minScale" in zoom_options else 0.3
            zoom_options["startScale"] = float(zoom_options["startScale"]) if "startScale" in zoom_options else 1.0
            zoom_options["wheel"] = True if "wheel" in zoom_options else False
            zoom_options["maxScale"] = float(zoom_options["maxScale"]) if "maxScale" in zoom_options else 3.0

        if "files" in problem_content:
            problem_content["files"] = [val for _, val in sorted(iter(problem_content["files"].items()), key=lambda x: int(x[0])) if val != ""]

        if "blocks_files" in problem_content:
            problem_content["blocks_files"] = [val for _, val in sorted(iter(problem_content["blocks_files"].items()), key=lambda x: int(x[0])) if val != ""]

        return problem_content

    @classmethod
    def get_text_fields(cls):
        return Problem.get_text_fields()

    def check_answer(self, _, __):
        return None, None, None, 0

    def input_is_consistent(self, task_input, default_allowed_extension, default_max_size):
        if not self.get_id() in task_input:
            return False

        # do not allow empty answers
        if len(task_input[self.get_id()]) == 0:
                return False
        return True


class DisplayableBlocklyProblem(BlocklyProblem, DisplayableProblem):

    """ A displayable blockly problem """
    def __init__(self, task, problemid, content, translations=None):
        super(DisplayableBlocklyProblem, self).__init__(task, problemid, content, translations)

    @classmethod
    def show_editbox(self, template_helper, key):
        return DisplayableBlocklyProblem.get_renderer(template_helper).editbox_blockly(key)

    @classmethod
    def show_editbox_templates(cls, template_helper, key):
        return DisplayableBlocklyProblem.get_renderer(template_helper).editbox_blockly_templates(key)

    @classmethod
    def get_renderer(cls, template_helper):
        """ Get the renderer for this class problem """
        return template_helper.get_custom_renderer(os.path.join(PATH_TO_PLUGIN, "templates"), False)

    @classmethod
    def get_type_name(self, gettext):
        return gettext("blockly")

    def adapt_input_for_backend(self, input_data):
        """ Adapt the input from web.py for the inginious.backend """
        return input_data

    def show_input(self, template_helper, language, seed):
        """ Show BlocklyBox """
        blockly_dico = dict()
        task = self.get_task()
        blockly_dico["courseid"] = task.get_course_id()
        blockly_dico["taskid"] = task.get_id()
        blockly_dico["filenames"] = []
        files = self._files + self._blocks_files
        blockly_dico["filenames"] = [str(filename) for filename in files]
        blockly_dico["toolbox"] = self._toolbox
        blockly_dico["id"] = self.get_id()
        blockly_dico["workspace"] = self._workspace
        blockly_dico["name"] = self.get_name()
        blockly_dico["options"] = json.dumps(self._options)
        return str(DisplayableBlocklyProblem.get_renderer(template_helper).box_blockly(blockly_dico,task))


def init(plugin_manager, course_factory, client, plugin_config):
    # TODO: Replace by shared static middleware and let webserver serve the files
    plugin_manager.add_page('/plugins/blockly/static/(.+)', StaticMockPage)
    plugin_manager.add_hook("css", lambda: "/plugins/blockly/static/css/blockly.css")
    plugin_manager.add_hook("javascript_header", lambda: "/plugins/blockly/static/studio_blockly.js")
    plugin_manager.add_hook("javascript_header", lambda: "/plugins/blockly/static/task_blockly.js")
    course_factory.get_task_factory().add_problem_type(DisplayableBlocklyProblem)
