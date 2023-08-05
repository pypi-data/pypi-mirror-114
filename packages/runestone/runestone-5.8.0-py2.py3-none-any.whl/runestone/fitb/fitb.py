# *********
# |docname|
# *********
#
# .. Copyright (C) 2013  Bradley N. Miller
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__author__ = "isaiahmayerchak"

import json
import ast
from numbers import Number
import re

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import logging

from runestone.server.componentdb import (
    addQuestionToDB,
    addHTMLToDB,
    maybeAddToAssignment,
)
from runestone.common import (
    RunestoneIdDirective,
    RunestoneNode,
    RunestoneIdNode,
    get_node_line,
)


def setup(app):
    app.add_directive("fillintheblank", FillInTheBlank)
    app.add_role("blank", BlankRole)
    app.add_node(FITBNode, html=(visit_fitb_node, depart_fitb_node))
    app.add_node(BlankNode, html=(visit_blank_node, depart_blank_node))
    app.add_node(
        FITBFeedbackNode, html=(visit_fitb_feedback_node, depart_fitb_feedback_node)
    )

    app.add_config_value("fitb_div_class", "runestone", "html")


class FITBNode(nodes.General, nodes.Element, RunestoneIdNode):
    def __init__(self, content, **kwargs):
        """

        Arguments:
        - `self`:
        - `content`:
        """
        super(FITBNode, self).__init__(**kwargs)
        self.runestone_options = content
        # Create a data structure of feedback.
        self.feedbackArray = []


def visit_fitb_node(self, node):

    node.delimiter = "_start__{}_".format(node.runestone_options["divid"])
    self.body.append(node.delimiter)

    res = node.template_start % node.runestone_options
    self.body.append(res)


def depart_fitb_node(self, node):
    # If there were fewer blanks than feedback items, add blanks at the end of the question.
    blankCount = 0
    for _ in node.traverse(BlankNode):
        blankCount += 1
    while blankCount < len(node.feedbackArray):
        visit_blank_node(self, None)
        blankCount += 1

    # Warn if there are fewer feedback items than blanks.
    if len(node.feedbackArray) < blankCount:
        # Taken from the example in the `logging API <http://www.sphinx-doc.org/en/stable/extdev/logging.html#logging-api>`_.
        logger = logging.getLogger(__name__)
        logger.warning(
            "Not enough feedback for the number of blanks supplied.", location=node
        )

    # Generate the HTML.
    json_feedback = json.dumps(node.feedbackArray)
    # Some nodes (for example, those in a timed node) have their ``document == None``. Find a valid ``document``.
    node_with_document = node
    while not node_with_document.document:
        node_with_document = node_with_document.parent
    # Supply client-side grading info if we're not grading on the server.
    node.runestone_options["json"] = (
        "false"
        if node_with_document.document.settings.env.config.runestone_server_side_grading
        else json_feedback
    )
    res = node.template_end % node.runestone_options
    self.body.append(res)

    # add HTML to the Database and clean up
    addHTMLToDB(
        node.runestone_options["divid"],
        node.runestone_options["basecourse"],
        "".join(self.body[self.body.index(node.delimiter) + 1 :]),
        json_feedback,
    )

    self.body.remove(node.delimiter)


class FillInTheBlank(RunestoneIdDirective):
    """
    .. fillintheblank:: some_unique_id_here

        Put the text of the question here.
        See https://runestone.academy/runestone/books/published/overview/Assessments/fitb.html
        for additional options and documentation.
        -   :Put the correct answer here: Put feedback displayed for this answer here.
            :x: Put feedback displayed for an incorrect answer here.
    """

    # config values (conf.py):
    #
    # - fitb_div_class - custom CSS class of the component's outermost div

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update(
        {
            "casei": directives.flag,  # case insensitive matching
        }
    )

    def run(self):
        """
            process the fillintheblank directive and generate html for output.
            :param self:
            :return: Nodes resulting from this directive.
            ...
            """

        super(FillInTheBlank, self).run()

        TEMPLATE_START = """
        <div class="%(divclass)s">
        <div data-component="fillintheblank" data-question_label="%(question_label)s" id="%(divid)s" %(optional)s style="visibility: hidden;">
            """

        TEMPLATE_END = """
        <script type="application/json">
            %(json)s
        </script>

        </div>
        </div>
            """

        addQuestionToDB(self)

        fitbNode = FITBNode(self.options, rawsource=self.block_text)
        fitbNode.source, fitbNode.line = self.state_machine.get_source_and_line(
            self.lineno
        )
        fitbNode.template_start = TEMPLATE_START
        fitbNode.template_end = TEMPLATE_END

        self.updateContent()

        self.state.nested_parse(self.content, self.content_offset, fitbNode)
        env = self.state.document.settings.env
        self.options["divclass"] = env.config.fitb_div_class

        # Expected _`structure`, with assigned variable names and transformations made:
        #
        # .. code-block::
        #   :number-lines:
        #
        #   fitbNode = FITBNode()
        #       Item 1 of problem text
        #       ...
        #       Item n of problem text
        #       feedback_bullet_list = bullet_list()  <-- The last element in fitbNode.
        #           feedback_list_item = list_item()   <-- Feedback for the first blank.
        #               feedback_field_list = field_list()
        #                   feedback_field = field()
        #                       feedback_field_name = field_name()  <-- Contains an answer.
        #                       feedback_field_body = field_body()  <-- Contains feedback for this answer.
        #                   feedback_field = field()  <-- Another answer/feedback pair.
        #           feedback_list_item = bullet_item()  <-- Feedback for the second blank.
        #               ...etc. ...
        #
        # This becomes a data structure:
        #
        # .. code-block::
        #   :number-lines:
        #
        #   self.feedbackArray = [
        #       [   # blankArray
        #           { # blankFeedbackDict: feedback 1
        #               "regex" : feedback_field_name   # (An answer, as a regex;
        #               "regexFlags" : "x"              # "i" if ``:casei:`` was specified, otherwise "".) OR
        #               "number" : [min, max]           # a range of correct numeric answers.
        #               "feedback": feedback_field_body (after being rendered as HTML)  # Provides feedback for this answer.
        #           },
        #           { # Feedback 2
        #               Same as above.
        #           }
        #       ],
        #       [  # Blank 2, same as above.
        #       ]
        #   ]
        #
        # ...and a transformed node structure:
        #
        # .. code-block::
        #   :number-lines:
        #
        #   fitbNode = FITBNode()
        #       Item 1 of problem text
        #       ...
        #       Item n of problem text
        #       FITBFeedbackNode(), which contains all the nodes in blank 1's feedback_field_body
        #       ...
        #       FITBFeedbackNode(), which contains all the nodes in blank n's feedback_field_body
        #
        self.assert_has_content()
        feedback_bullet_list = fitbNode.pop()
        if not isinstance(feedback_bullet_list, nodes.bullet_list):
            raise self.error(
                "On line {}, the last item in a fill-in-the-blank question must be a bulleted list.".format(
                    get_node_line(feedback_bullet_list)
                )
            )
        for feedback_list_item in feedback_bullet_list.children:
            assert isinstance(feedback_list_item, nodes.list_item)
            feedback_field_list = feedback_list_item[0]
            if len(feedback_list_item) != 1 or not isinstance(
                feedback_field_list, nodes.field_list
            ):
                raise self.error(
                    "On line {}, each list item in a fill-in-the-blank problems must contain only one item, a field list.".format(
                        get_node_line(feedback_list_item)
                    )
                )
            blankArray = []
            for feedback_field in feedback_field_list:
                assert isinstance(feedback_field, nodes.field)

                feedback_field_name = feedback_field[0]
                assert isinstance(feedback_field_name, nodes.field_name)
                feedback_field_name_raw = feedback_field_name.rawsource
                # See if this is a number, optinonally followed by a tolerance.
                try:
                    # Parse the number. In Python 3 syntax, this would be ``str_num, *list_tol = feedback_field_name_raw.split()``.
                    tmp = feedback_field_name_raw.split()
                    str_num = tmp[0]
                    list_tol = tmp[1:]
                    num = ast.literal_eval(str_num)
                    assert isinstance(num, Number)
                    # If no tolerance is given, use a tolarance of 0.
                    if len(list_tol) == 0:
                        tol = 0
                    else:
                        assert len(list_tol) == 1
                        tol = ast.literal_eval(list_tol[0])
                        assert isinstance(tol, Number)
                    # We have the number and a tolerance. Save that.
                    blankFeedbackDict = {"number": [num - tol, num + tol]}
                except (SyntaxError, ValueError, AssertionError):
                    # We can't parse this as a number, so assume it's a regex.
                    regex = (
                        # The given regex must match the entire string, from the beginning (which may be preceded by whitespaces) ...
                        r"^\s*"
                        +
                        # ... to the contents (where a single space in the provided pattern is treated as one or more whitespaces in the student's answer) ...
                        feedback_field_name.rawsource.replace(" ", r"\s+")
                        # ... to the end (also with optional spaces).
                        + r"\s*$"
                    )
                    blankFeedbackDict = {
                        "regex": regex,
                        "regexFlags": "i" if "casei" in self.options else "",
                    }
                    # Test out the regex to make sure it compiles without an error.
                    try:
                        re.compile(regex)
                    except Exception as ex:
                        raise self.error(
                            'Error when compiling regex "{}": {}.'.format(
                                regex, str(ex)
                            )
                        )
                blankArray.append(blankFeedbackDict)

                feedback_field_body = feedback_field[1]
                assert isinstance(feedback_field_body, nodes.field_body)
                # Append feedback for this answer to the end of the fitbNode.
                ffn = FITBFeedbackNode(
                    feedback_field_body.rawsource,
                    *feedback_field_body.children,
                    **feedback_field_body.attributes
                )
                ffn.blankFeedbackDict = blankFeedbackDict
                fitbNode += ffn

            # Add all the feedback for this blank to the feedbackArray.
            fitbNode.feedbackArray.append(blankArray)

        maybeAddToAssignment(self)

        return [fitbNode]


# BlankRole
# ---------
# Create role representing the blank in a fill-in-the-blank question. This function returns a tuple of two values:
#
# 0. A list of nodes which will be inserted into the document tree at the point where the interpreted role was encountered (can be an empty list).
# #. A list of system messages, which will be inserted into the document tree immediately after the end of the current block (can also be empty).
def BlankRole(
    # _`roleName`: the local name of the interpreted role, the role name actually used in the document.
    roleName,
    # _`rawtext` is a string containing the enitre interpreted text input, including the role and markup. Return it as a problematic node linked to a system message if a problem is encountered.
    rawtext,
    # The interpreted _`text` content.
    text,
    # The line number (_`lineno`) where the interpreted text begins.
    lineno,
    # _`inliner` is the docutils.parsers.rst.states.Inliner object that called this function. It contains the several attributes useful for error reporting and document tree access.
    inliner,
    # A dictionary of directive _`options` for customization (from the "role" directive), to be interpreted by this function. Used for additional attributes for the generated elements and other functionality.
    options={},
    # A list of strings, the directive _`content` for customization (from the "role" directive). To be interpreted by the role function.
    content=[],
):

    # Blanks ignore all arguments, just inserting a blank.
    blank_node = BlankNode(rawtext)
    blank_node.line = lineno
    return [blank_node], []


class BlankNode(nodes.Inline, nodes.TextElement, RunestoneNode):
    pass


def visit_blank_node(self, node):
    self.body.append('<input type="text">')


def depart_blank_node(self, node):
    pass


# Contains feedback for one answer.
class FITBFeedbackNode(nodes.General, nodes.Element, RunestoneNode):
    pass


def visit_fitb_feedback_node(self, node):
    # Save the HTML generated thus far. Anything generated under this node will be placed in JSON.
    self.context.append(self.body)
    self.body = []


def depart_fitb_feedback_node(self, node):
    # Place all the HTML generated for this node and its children into the feedbackArray.
    node.blankFeedbackDict["feedback"] = "".join(self.body)
    # Restore HTML generated thus far.
    self.body = self.context.pop()
