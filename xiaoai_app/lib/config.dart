/// App configuration. Change these before building.
class AppConfig {
  /// World Server URL (HTTP)
  static const serverUrl = String.fromEnvironment(
    'SERVER_URL',
    defaultValue: 'http://10.0.2.2:8080', // Android emulator -> host machine
  );

  /// World Server WebSocket URL
  static String get wsUrl => serverUrl.replaceFirst('http', 'ws');

  /// Seconds before switching from engaged back to idle
  static const engagedTimeout = 15;
}
