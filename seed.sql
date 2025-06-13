-- 既存のテーブルが存在する場合は削除
DROP TABLE IF EXISTS keypoints;
DROP TABLE IF EXISTS timelines;
DROP TABLE IF EXISTS consultations;

-- consultationsテーブルの作成
CREATE TABLE consultations (
    consultation_id INT PRIMARY KEY,
    dictation_text TEXT NULL COMMENT '文字起こしテキスト（最大65535文字）',
    summary_text TEXT NULL COMMENT '要約テキスト（最大1023文字）',
    audio_file_path VARCHAR(255) NULL COMMENT '音声ファイルのパス',
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);

-- timelinesテーブルの作成
CREATE TABLE timelines (
    consultation_id INT,
    seq SMALLINT,
    timeseries_text TEXT COMMENT '時系列テキスト（最大1023文字）',
    start_dt DATETIME COMMENT '開始時間',
    end_dt DATETIME COMMENT '終了時間',
    f_bookmark TINYINT DEFAULT 0 COMMENT 'しおりフラグ',
    PRIMARY KEY (consultation_id, seq),
    FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON DELETE CASCADE
);

-- keypointsテーブルの作成
CREATE TABLE keypoints (
    consultation_id INT,
    seq SMALLINT,
    keypoint_text TEXT COMMENT 'キーポイントテキスト（最大1023文字）',
    PRIMARY KEY (consultation_id, seq),
    FOREIGN KEY (consultation_id) REFERENCES consultations(consultation_id) ON DELETE CASCADE
);