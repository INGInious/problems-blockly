# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

import os
import web
import json

from inginious.common.tasks_code_boxes import MultilineBox
from inginious.common.tasks_problems import CodeProblem
from inginious.frontend.task_problems import DisplayableCodeProblem
from inginious.frontend.tasks_code_boxes import DisplayableBox

__version__ = "0.1.dev0"

PATH_TO_PLUGIN = os.path.abspath(os.path.dirname(__file__))


class StaticMockPage(object):
    # TODO: Replace by shared static middleware and let webserver serve the files
    def GET(self, path):
        if not os.path.abspath(PATH_TO_PLUGIN) in os.path.abspath(os.path.join(PATH_TO_PLUGIN, path)):
            raise web.notfound()

        try:
            with open(os.path.join(PATH_TO_PLUGIN, "static", path), 'r') as file:
                return file.read()
        except:
            raise web.notfound()

    def POST(self, path):
        return self.GET(path)


class BlocklyProblem(CodeProblem):
    """
    Blockly problem
    """
    def __init__(self, task, problemid, content, translations=None):
        super(BlocklyProblem, self).__init__(task, problemid, content, translations)
        self._box_types.update({"blockly": BlocklyBox})
        self._boxes = [self._create_box("", {"type": "blockly",
                                             "language": content["language"],
                                             "optional": content.get("optional", False),
                                             "toolbox": content.get("toolbox", ""),
                                             "files": content.get("files", []),
                                             "blocks_files": content.get("blocks_files", []),
                                             "options": content.get("options", []),
                                             "workspace": content.get("workspace", ""),
                                            })]

    @classmethod
    def get_type(self):
        return "blockly"

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
        return CodeProblem.get_text_fields()


class BlocklyBox(MultilineBox):
    """
        Blockly box.
    """
    def get_type(self):
        return "blockly"

    def __init__(self, problem, boxid, boxData):
        super(BlocklyBox, self).__init__(problem, boxid, boxData)
        if "toolbox" in boxData:
            self._toolbox = boxData["toolbox"]
        else:
            self._toolbox = "<xml></xml>"
        if "workspace" in boxData:
            self._workspace = boxData["workspace"]
        if "options" in boxData:
            self._options = boxData["options"]
        if "files" in boxData:
            self._files = boxData["files"]
        if "blocks_files" in boxData:
            self._blocks_files = boxData["blocks_files"]

    def input_is_consistent(self, taskInput, default_allowed_extension, default_max_size):
        return MultilineBox.input_is_consistent(self, taskInput, default_allowed_extension, default_max_size)


class DisplayableBlocklyProblem(BlocklyProblem, DisplayableCodeProblem):
    """ A displayable blockly problem """
    def __init__(self, task, problemid, content, translations=None):
        super(DisplayableBlocklyProblem, self).__init__(task, problemid, content, translations)
        self._box_types.update({"blockly": DisplayableBlocklyBox})
        self._boxes = [self._create_box("", {"type": "blockly",
                                             "language": content["language"],
                                             "optional": content.get("optional", False),
                                             "toolbox": content.get("toolbox", ""),
                                             "files": content.get("files", []),
                                             "blocks_files": content.get("blocks_files", []),
                                             "options": content.get("options", []),
                                             "workspace": content.get("workspace", ""),
                                             })]

    @classmethod
    def show_editbox(self, template_helper, key):
        return DisplayableBlocklyProblem.get_renderer(template_helper).editbox_blockly(key)

    @classmethod
    def get_renderer(cls, template_helper):
        """ Get the renderer for this class problem """
        return template_helper.get_custom_renderer(os.path.join(PATH_TO_PLUGIN, "templates"), False)

    @classmethod
    def get_type_name(self, gettext):
        return gettext("blockly")


class DisplayableBlocklyBox(BlocklyBox, DisplayableBox):
    """ A displayable blockly box """
    def __init__(self, problem, boxid, boxData):
        super(DisplayableBlocklyBox, self).__init__(problem, boxid, boxData)

    def adapt_input_for_backend(self, input_data):
        """ Adapt the input from web.py for the inginious.backend """
        return input_data

    @classmethod
    def get_renderer(cls, template_helper):
        """ Get the renderer for this class problem """
        return template_helper.get_custom_renderer(os.path.join(PATH_TO_PLUGIN, "templates"), False)

    def show(self, template_helper, language):
        """ Show BlocklyBox """
        task = self.get_problem().get_task()
        courseid = task.get_course_id()
        taskid = task.get_id()
        filenames = []
        for filename in self._files + self._blocks_files:
            filenames.append(str(taskid) + "/" + str(filename))
        toolbox = self._toolbox
        return str(DisplayableBlocklyBox.get_renderer(template_helper).box_blockly(courseid, taskid, self.get_complete_id(), self.get_problem().get_name(), self._language, toolbox, filenames, self._workspace, json.dumps(self._options)))


def init(plugin_manager, course_factory, client, plugin_config):
    # TODO: Replace by shared static middleware and let webserver serve the files
    plugin_manager.add_page('/plugins/blockly/static/(.+)', StaticMockPage)
    plugin_manager.add_hook("css", lambda: "/plugins/blockly/static/css/blockly.css")
    plugin_manager.add_hook("javascript_header", lambda: "/plugins/blockly/static/studio_blockly.js")
    plugin_manager.add_hook("javascript_header", lambda: "/plugins/blockly/static/task_blockly.js")
    course_factory.get_task_factory().add_problem_type(DisplayableBlocklyProblem)
