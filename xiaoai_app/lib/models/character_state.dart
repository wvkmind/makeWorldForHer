class CharacterState {
  String action;
  String expression;
  String scene;
  String mood;
  String timeOfDay;
  String outfit;
  bool engaged;

  CharacterState({
    this.action = 'standing',
    this.expression = 'smile',
    this.scene = 'living_room',
    this.mood = 'happy',
    this.timeOfDay = 'day',
    this.outfit = 'H07',
    this.engaged = false,
  });

  String get spriteKey => '${action}_$expression';
  String get viewMode => engaged ? 'engaged' : 'idle';
  String get sceneKey => '${scene}_${spriteKey}_${viewMode}_$timeOfDay';

  bool get hasAnimation => _animatedStates.contains('${spriteKey}_$viewMode');

  static const _animatedStates = <String>{};

  factory CharacterState.fromJson(Map<String, dynamic> json) {
    return CharacterState(
      action: json['action'] ?? 'standing',
      expression: json['expression'] ?? 'smile',
      scene: json['scene'] ?? 'living_room',
      mood: json['mood'] ?? 'happy',
      timeOfDay: json['time_of_day'] ?? 'day',
      outfit: json['outfit'] ?? 'H07',
      engaged: json['engaged'] ?? false,
    );
  }

  void applyUpdate(Map<String, dynamic> update) {
    if (update['action'] != null) action = update['action'];
    if (update['expression'] != null) expression = update['expression'];
    if (update['scene'] != null) scene = update['scene'];
    if (update['mood'] != null) mood = update['mood'];
    if (update['time_of_day'] != null) timeOfDay = update['time_of_day'];
    if (update['outfit'] != null) outfit = update['outfit'];
    if (update['engaged'] != null) engaged = update['engaged'];
  }

  Map<String, dynamic> toJson() => {
    'action': action,
    'expression': expression,
    'scene': scene,
    'mood': mood,
    'time_of_day': timeOfDay,
    'outfit': outfit,
    'engaged': engaged,
  };
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime time;

  ChatMessage({required this.text, required this.isUser, DateTime? time})
      : time = time ?? DateTime.now();
}
