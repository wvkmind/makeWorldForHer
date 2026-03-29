import 'package:flutter/material.dart';
import '../models/character_state.dart';
import 'frame_animation.dart';

class SceneView extends StatefulWidget {
  final String scene;
  final CharacterState state;
  final bool isActive;

  const SceneView({
    super.key,
    required this.scene,
    required this.state,
    this.isActive = false,
  });

  @override
  State<SceneView> createState() => _SceneViewState();
}

class _SceneViewState extends State<SceneView> {
  double _panX = 0;

  @override
  Widget build(BuildContext context) {
    final screenW = MediaQuery.of(context).size.width;
    final screenH = MediaQuery.of(context).size.height * 0.65;
    // Image is wider than screen, calculate scaled width
    // Assuming source image is ~1024x768, fill height then allow pan
    final imageAspect = 1024.0 / 768.0;
    final scaledW = screenH * imageAspect;
    final maxPan = (scaledW - screenW).clamp(0.0, double.infinity);

    final showCharacter = widget.isActive && widget.state.scene == widget.scene;
    final sceneKey = widget.state.sceneKey;

    return Stack(
      children: [
        // Pannable scene area
        GestureDetector(
          onHorizontalDragUpdate: (d) {
            setState(() {
              _panX = (_panX - d.delta.dx).clamp(0.0, maxPan);
            });
          },
          child: ClipRect(
            child: SizedBox(
              width: screenW,
              height: screenH,
              child: OverflowBox(
                maxWidth: scaledW,
                maxHeight: screenH,
                alignment: Alignment.topLeft,
                child: Transform.translate(
                  offset: Offset(-_panX, 0),
                  child: SizedBox(
                    width: scaledW,
                    height: screenH,
                    child: _buildContent(sceneKey, showCharacter, scaledW, screenH),
                  ),
                ),
              ),
            ),
          ),
        ),
        // Room label
        Positioned(
          top: 12,
          left: 16,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: Colors.black26,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              _sceneName(widget.scene),
              style: const TextStyle(color: Colors.white70, fontSize: 13),
            ),
          ),
        ),
        // Time overlay
        Positioned.fill(
          child: IgnorePointer(
            child: Container(color: _timeOverlay(widget.state.timeOfDay)),
          ),
        ),
        // Pan indicator dots
        Positioned(
          bottom: 8,
          left: 0,
          right: 0,
          child: Center(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: Colors.black26,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                maxPan > 0 ? '← 左右滑动查看 →' : '',
                style: const TextStyle(color: Colors.white38, fontSize: 11),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildContent(String sceneKey, bool showChar, double w, double h) {
    final hasFrames = widget.state.hasAnimation;

    // Try integrated scene (character baked into background)
    if (showChar) {
      if (hasFrames) {
        return FrameAnimation(
          framesDir: 'frames/$sceneKey',
          frameCount: 60,
          fps: 12,
          fit: BoxFit.cover,
        );
      }
      // Static integrated scene
      return Image.asset(
        'assets/scenes/$sceneKey.png',
        width: w,
        height: h,
        fit: BoxFit.cover,
        errorBuilder: (_, __, ___) => _fallback(showChar, w, h),
      );
    }
    return _fallback(showChar, w, h);
  }

  /// Background + overlaid character sprite
  Widget _fallback(bool showChar, double w, double h) {
    return Stack(
      children: [
        // Room background
        Image.asset(
          'assets/backgrounds/bg_${widget.scene}.png',
          width: w,
          height: h,
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => Container(
            width: w,
            height: h,
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: _sceneGradient(widget.scene),
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(_sceneIcon(widget.scene), size: 48, color: Colors.white30),
                const SizedBox(height: 8),
                Text(_sceneName(widget.scene),
                    style: const TextStyle(color: Colors.white38, fontSize: 18)),
              ],
            ),
          ),
        ),
        // Character sprite overlay
        if (showChar)
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Center(
              child: Image.asset(
                'assets/sprites/character/${widget.state.spriteKey}.png',
                height: h * 0.8,
                fit: BoxFit.contain,
                errorBuilder: (_, __, ___) => const SizedBox.shrink(),
              ),
            ),
          ),
      ],
    );
  }

  String _sceneName(String s) => const {
    'living_room': '客厅', 'bedroom': '卧室', 'kitchen': '厨房',
    'bathroom': '卫生间', 'balcony': '阳台',
  }[s] ?? s;

  IconData _sceneIcon(String s) => const {
    'living_room': Icons.weekend, 'bedroom': Icons.bed,
    'kitchen': Icons.kitchen, 'bathroom': Icons.bathtub,
    'balcony': Icons.balcony,
  }[s] ?? Icons.home;

  List<Color> _sceneGradient(String s) {
    switch (s) {
      case 'bedroom': return [const Color(0xFF4A148C), const Color(0xFF2D1B4E)];
      case 'living_room': return [const Color(0xFF5D4037), const Color(0xFF3E2723)];
      case 'kitchen': return [const Color(0xFF33691E), const Color(0xFF1B5E20)];
      case 'bathroom': return [const Color(0xFF006064), const Color(0xFF004D40)];
      case 'balcony': return [const Color(0xFF1565C0), const Color(0xFF0D47A1)];
      default: return [const Color(0xFF455A64), const Color(0xFF37474F)];
    }
  }

  Color _timeOverlay(String time) {
    switch (time) {
      case 'morning': return Colors.amber.withValues(alpha: 0.1);
      case 'evening': return Colors.orange.withValues(alpha: 0.15);
      case 'night': return Colors.indigo.withValues(alpha: 0.3);
      default: return Colors.transparent;
    }
  }
}
