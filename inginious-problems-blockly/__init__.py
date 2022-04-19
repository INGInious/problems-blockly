# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

import os
import os.path
import gettext
from flask import send_from_directory
import json

from inginious.common.tasks_problems import Problem
from inginious.frontend.pages.utils import INGIniousPage
from inginious.frontend.task_problems import DisplayableProblem

__version__ = "0.1.dev0"

PATH_TO_PLUGIN = os.path.dirname(os.path.abspath(__file__))
PATH_TO_TEMPLATES = os.path.join(PATH_TO_PLUGIN, "templates")
_translations = None


class StaticMockPage(INGIniousPage):

    def GET(self, path):
        return send_from_directory(os.path.join(PATH_TO_PLUGIN, "static"), path)

    def POST(self, path):
        return self.GET(path)


class BlocklyProblem(Problem):
    """
    Blockly problem
    """

    def __init__(self, problemid, content, translations, taskfs):
        super(BlocklyProblem, self).__init__(problemid, content, translations, taskfs)
        self._task_fs = taskfs
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
                               'oneBasedIndex', 'readOnly', 'rtl', 'scrollbars', 'sounds']
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
            problem_content["files"] = [val for _, val in
                                        sorted(iter(problem_content["files"].items()), key=lambda x: int(x[0])) if
                                        val != ""]

        if "blocks_files" in problem_content:
            problem_content["blocks_files"] = [val for _, val in sorted(iter(problem_content["blocks_files"].items()),
                                                                        key=lambda x: int(x[0])) if val != ""]

        return problem_content

    @classmethod
    def get_text_fields(cls):
        return Problem.get_text_fields()

    def check_answer(self, _, __):
        return None, None, None, 0, ""

    def input_is_consistent(self, task_input, default_allowed_extension, default_max_size):
        if not self.get_id() in task_input:
            return False

        # do not allow empty answers
        if len(task_input[self.get_id()]) == 0:
            return False
        return True


class DisplayableBlocklyProblem(BlocklyProblem, DisplayableProblem):
    """ A displayable blockly problem """

    def __init__(self, problemid, content, translations, taskfs):
        super(DisplayableBlocklyProblem, self).__init__(problemid, content, translations, taskfs)

    @classmethod
    def show_editbox(self, template_helper, key, language):
        translation = _translations.get(language, gettext.NullTranslations())
        return template_helper.render("editbox_blockly.html", gettext=translation.gettext, template_folder=PATH_TO_TEMPLATES, key=key)

    @classmethod
    def show_editbox_templates(cls, template_helper, key, language):
        translation = _translations.get(language, gettext.NullTranslations())
        return template_helper.render("editbox_blockly_templates.html", gettext=translation.gettext, template_folder=PATH_TO_TEMPLATES, key=key)

    @classmethod
    def get_type_name(self, language):
        return "blockly"

    def adapt_input_for_backend(self, input_data):
        """ Adapt the input from web.py for the inginious.backend """
        return input_data

    def show_input(self, template_helper, language, seed):
        """ Show BlocklyBox """
        blockly_dico = dict()
        coursedir, taskid = os.path.split(self._task_fs.prefix.rstrip("/"))
        blockly_dico["taskid"] = taskid
        blockly_dico["courseid"] = os.path.split(coursedir)[1]
        blockly_dico["filenames"] = []
        files = self._files + self._blocks_files
        blockly_dico["filenames"] = [str(filename) for filename in files]
        blockly_dico["toolbox"] = self._toolbox
        blockly_dico["id"] = self.get_id()
        blockly_dico["workspace"] = self._workspace
        blockly_dico["name"] = self.get_name()
        blockly_dico["options"] = json.dumps(self._options)
        translation = _translations.get(language, gettext.NullTranslations())
        static_msg_exist = os.path.exists(PATH_TO_PLUGIN+"/static/blockly/msg/js/"+language+".js")
        return str(
            template_helper.render("box_blockly.html", template_folder=PATH_TO_TEMPLATES,
                                   blockly_dico=(blockly_dico),
                                   gettext=translation.gettext,
                                   static_msg_exist=static_msg_exist
                                   ))


def init(plugin_manager, course_factory, client, plugin_config):
    global _translations
    plugin_manager.add_page('/plugins/blockly/static/<path:path>', StaticMockPage.as_view('blocklystaticpage'))
    plugin_manager.add_hook("css", lambda: "/plugins/blockly/static/css/blockly.css")
    plugin_manager.add_hook("javascript_header", lambda: "/plugins/blockly/static/studio_blockly.js")
    plugin_manager.add_hook("javascript_header", lambda: "/plugins/blockly/static/task_blockly.js")
    course_factory.get_task_factory().add_problem_type(DisplayableBlocklyProblem)

    # Init gettext
    languages = ["en", "fr"]
    _translations = {
         lang: gettext.translation('messages', PATH_TO_PLUGIN + '/i18n', [lang]) for lang in languages
    }
