extends Node2D

@onready var dialogue_label: Label = $Label
@onready var save_button: Button = $SaveButton
@onready var choices_box: VBoxContainer = $Choices
var api_base := "http://127.0.0.1:8000"

func _ready() -> void:
	print("🎭 Kontrapunkt MVP running (Godot 4 Vulkan)")
	save_button.pressed.connect(_on_save_pressed)
	_fetch_dialogue()

func _fetch_dialogue() -> void:
	var http := HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(_on_http_request_completed)
	var payload := {
		"state": {"skills": {"sensual_intelligence": 0.6, "obscura_sensitivity": 0.5}},
		"input": "hello"
	}
	var err = http.request(api_base + "/dialogue/respond", HTTPClient.METHOD_POST, ["Content-Type: application/json"], JSON.stringify(payload))
	if err != OK:
		push_error("HTTP request failed: %s" % err)

func _on_http_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if typeof(json) == TYPE_DICTIONARY and json.has("text"):
			dialogue_label.text = str(json["text"])
			_render_choices(json.get("branches", {}))
		else:
			print("Dialogue:", json)
	else:
		push_warning("API error: %s" % response_code)

func _on_save_pressed() -> void:
	var snapshot := {
	"player": {"pos": {"x": 0, "y": 0}},
		"scene": "Main",
		"skills": {"sensual_intelligence": 0.6, "obscura_sensitivity": 0.5}
	}
	var http := HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(_on_save_completed)
	var err = http.request(api_base + "/save/write", HTTPClient.METHOD_POST, ["Content-Type: application/json"], JSON.stringify({"snapshot": snapshot}))
	if err != OK:
		push_error("Save request failed: %s" % err)

func _on_save_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if typeof(json) == TYPE_DICTIONARY and json.has("ok") and json["ok"]:
			save_button.text = "Saved ✓"
		else:
			push_warning("Save response unexpected: %s" % body.get_string_from_utf8())
	else:
		push_warning("Save API error: %s" % response_code)

func _render_choices(branches: Dictionary) -> void:
	for c in choices_box.get_children():
		c.queue_free()
	for key in branches.keys():
		var b := Button.new()
		b.text = str(branches[key])
		b.pressed.connect(func(): _choose_branch(key))
		choices_box.add_child(b)

func _choose_branch(key: String) -> void:
	var http := HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(_on_http_request_completed)
	var payload := {
		"state": {"skills": {"sensual_intelligence": 0.6, "obscura_sensitivity": 0.5}},
		"input": key
	}
	var err = http.request(api_base + "/dialogue/respond", HTTPClient.METHOD_POST, ["Content-Type: application/json"], JSON.stringify(payload))
	if err != OK:
		push_error("HTTP request failed: %s" % err)
