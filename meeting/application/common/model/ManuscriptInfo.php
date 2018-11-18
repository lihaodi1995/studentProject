<?php
namespace app\common\model;

use think\Model;

class ManuscriptInfo extends Model {
    protected $pk = 'manuscript_info_id';

    public function manuscript() {
        return $this->belongsTo('Manuscript');
    }
}
