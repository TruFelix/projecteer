import 'dart:io';

import 'package:mason/mason.dart';
import 'package:yaml/yaml.dart';

void debugPrintStart(List<String> arguments) {
  print("Arguments: $arguments");
}

void main(List<String> arguments) {
  debugPrintStart(arguments);

  final config = Config.parseConfigFile();
  print(config);

  final generator = MasonGenerator("My Id", "Some description", files: config.templates);

  generator.generate(DirectoryGeneratorTarget(Directory.current), vars: config.vars);
}

class Config {
  final List<String> sourceFiles;
  final Map<String, String> vars;

  /// Create a Config with specifing all properties explicitly.
  const Config({required this.sourceFiles, this.vars = const <String, String>{}});

  static final standard = Config(
      sourceFiles: Directory.current
          .listSync(recursive: true)
          .where((element) => element.path.contains(".template"))
          .map((e) => e.path)
          .toList());

  /// Create a Config using a config file at the specified [path].
  factory Config.parseConfigFile({String path = "project-config.yaml"}) {
    Config tmp = standard;

    final configFile = File(path);
    if (!configFile.existsSync()) {
      return tmp;
    }

    final configContents = configFile.readAsStringSync();
    final parsedConfig = loadYaml(configContents);
    print(parsedConfig);
    print(parsedConfig["variables"]);

    return tmp.copyWith(sourceFiles: parsedConfig?["sourceFiles"] ?? []);
  }

  List<TemplateFile> get templates => sourceFiles
      .map((e) => TemplateFile(
            e,
            File(e).readAsStringSync(),
          ))
      .toList();

  copyWith({List<String>? sourceFiles}) => Config(sourceFiles: sourceFiles ?? this.sourceFiles);
}
