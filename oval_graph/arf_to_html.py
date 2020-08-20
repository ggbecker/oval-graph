from datetime import datetime


from .client import Client
from .converter import Converter
from .exceptions import NotChecked


class ArfToHtml(Client):
    def __init__(self, args):
        super().__init__(args)
        self.off_webbrowser = self.arg.off_web_browser
        self.show_failed_rules = self.arg.show_failed_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.all_in_one = self.arg.all_in_one
        if self.all_in_one:
            self.all_rules = True

    def _get_message(self):
        MESSAGES = {
            'description': 'Client for visualization of SCAP rule evaluation results',
            '--output': 'The directory where to save output directory with files.',
            'source_filename': 'ARF scan file',
        }
        return MESSAGES

    def create_dict_of_rule(self, rule_id):
        converter = Converter(self.xml_parser.get_oval_tree(rule_id))
        return converter.to_JsTree_dict(self.hide_passing_tests)

    def _prepare_all_in_one_data(self, rules, dict_oval_trees, out, date):
        for rule in rules['rules']:
            try:
                dict_oval_trees[
                    'graph-of-' + rule + date] = self.create_dict_of_rule(rule)
            except NotChecked as error:
                self.print_red_text(error)
        src = self.get_save_src('rules')
        self.save_html_with_all_rules_in_one(
            dict_oval_trees, src, rules, out)
        return out

    def _prepare_data_by_one(self, rules, dict_oval_trees, out, date):
        for rule in rules['rules']:
            try:
                oval_tree_dict = self.create_dict_of_rule(rule)
                src = self.get_save_src(rule)
                self.save_html_and_open_html(
                    oval_tree_dict, src, rule, out)
            except NotChecked as error:
                self.print_red_text(error)
        return out

    def prepare_data(self, rules):
        out = []
        dict_oval_trees = dict()
        date = str(datetime.now().strftime("-%d_%m_%Y-%H_%M_%S"))
        if self.all_in_one:
            out = self._prepare_all_in_one_data(
                rules, dict_oval_trees, out, date)
        else:
            out = self._prepare_data_by_one(rules, dict_oval_trees, out, date)
        return out

    def prepare_parser(self):
        super().prepare_parser()
        self.parser.add_argument(
            '--all-in-one',
            action="store_true",
            default=False,
            help="Processes all rules into one file.")
        self.parser.add_argument(
            '--off-web-browser',
            action="store_true",
            default=False,
            help="It does not start the web browser.")
        self.parser.add_argument(
            '--show-failed-rules',
            action="store_true",
            default=False,
            help="Show only FAILED rules")
        self.parser.add_argument(
            '--show-not-selected-rules',
            action="store_true",
            default=False,
            help="Show notselected rules. These rules will not be visualized.")
